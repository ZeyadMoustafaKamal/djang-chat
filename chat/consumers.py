from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from channels_redis.core import RedisChannelLayer

from .models import Message

import json
import asyncio

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    """ The consumer is just a link to send a receive data and since I will store all messages I will not have 
        make the users join the same "group" every time so I will create a group named "from{user1.id}_to{user2.id}"
        and the user1 is the first user to open a connection and the user2 is the second user to open a connection
        so I will create this group and when another users opens a connection I will connect him with the first group 
        Just see the code and you will understand what I mean"""
    async def connect(self):
        self.sender = self.scope['user']
        
        receiver_id = self.scope['url_route']['kwargs']['user_id']
        self.receiver = await self.get_user(receiver_id)
        self.group_name = 'none' # if I didn't add this line, it will cause an issue if the below "if condition" was True
        if not self.receiver or not self.sender:
            self.close()
            return
        
        self.group_name = await self.get_group_name(self.sender.id, receiver_id)

        await self.set_user_to_group(self.group_name, self.sender.id)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def get_group_name(self, sender_id, receiver_id):
        """ this function will get the suitable group name to use it in connection proccess """
        group_name_1 = f"from{receiver_id}_to{sender_id}"
        group_name_2 = f"from{sender_id}_to{receiver_id}"

        group_1 = await self.get_users_from_group(group_name_1)
        if group_1:
            return group_name_1
        return group_name_2
    
    @database_sync_to_async
    def get_user(self, id):
        return User.objects.filter(id=id).first()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        await self.remove_user_from_group(self.group_name, self.sender.id)
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        receiver_id = self.receiver.id 
        receiver_type = await database_sync_to_async(ContentType.objects.get_for_model)(User)

        await database_sync_to_async(Message.objects.create)(
            sender=self.sender,
            receiver_type=receiver_type,
            receiver_id=receiver_id,
            content=message
        )
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'send_message',
                'message':message,
                'sender_id':self.sender.id
            }
        )
    async def send_message(self, event):
        message = event['message']

        sender_image = await database_sync_to_async(lambda: self.sender.profile.picture.url)()
        await self.send(
            text_data=json.dumps({
                'message':message,
                'sender_id':event['sender_id'],
                'sender_image':sender_image,
                'sender_username':self.sender.username
            })
        )
    @database_sync_to_async
    def set_user_to_group(self, key, value):
        async def set_users_async():
            connection = self.channel_layer.connection(self.channel_layer.consistent_hash(key))
            await connection.lpush(key, value)

        asyncio.run(set_users_async())

    async def get_users_from_group(self, key):
        connection = await self.channel_layer.connection(self.channel_layer.consistent_hash(key))
        user_bytes = await connection.lrange(key, 0, -1)
        users = [user.decode('utf-8') for user in user_bytes]
        unique_users = list(set(users))
        return unique_users

    @database_sync_to_async
    def remove_user_from_group(self, key, value):
        async def remove_user_async():
            connection = self.channel_layer.connection(self.channel_layer.consistent_hash(key))
            await connection.lrem(key, 0, value)
        asyncio.run(remove_user_async())



