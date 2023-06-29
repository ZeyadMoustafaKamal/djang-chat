from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404

User = get_user_model()

def index(request):
    return render(request, 'index.html', )

def room(request, room_name):
    return render(request, 'chatroom.html',{'room_name':room_name} )

def search(request):
    context = {}
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        users = User.objects.filter(Q(id=keyword) | Q(username=keyword)).exclude(id=request.user.id)
        context['users'] = users
    return render(request, 'search.html', context)

def user_profile(request, user_name):
    if user_name.startswith('@'):
        user_name = user_name[1:]
    user_obj = get_object_or_404(User, username=user_name)
    return render(request, 'userprofile.html', {'user_obj':user_obj})