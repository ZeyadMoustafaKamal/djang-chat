from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')

    # This will replace the normal foreignkey because in the future I will create group chats and as the groups will be defferent and I should 
    # implement another model in the database in order to store data like the group name and the members and date created I found that using
    # generic foreignkey will be very suitable for this

    receiver_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    receiver_id = models.PositiveIntegerField()
    receiver_object = GenericForeignKey("receiver_type", "receiver_id")
    
    content = models.CharField(max_length=250, blank=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.content} at {self.date_sent}'

