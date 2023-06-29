from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from .models import Message

User = get_user_model()

@login_required
def chat(request, user_id):

    context = {}
    receiver_type = ContentType.objects.get_for_model(User)
                                    # This query took me hours to reach
    messages = Message.objects.filter((Q(receiver_id=user_id) & Q(receiver_type=receiver_type) & Q(sender__id=request.user.id)) |
                                       Q(sender__id=user_id, receiver_type=receiver_type, receiver_id=request.user.id))\
                                        .order_by('date_sent')

    context['messages'] = messages
    context['user_id'] = user_id

    return render(request, 'chat.html', context)