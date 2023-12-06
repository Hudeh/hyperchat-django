from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import ChatRoom, Message


@login_required
def chat_rooms(request):
    rooms = ChatRoom.objects.all()

    return render(request, "chat/chat_rooms.html", {"rooms": rooms})


@login_required
def messages(request, slug):
    chat_room = ChatRoom.objects.get(slug=slug)
    messages = Message.objects.filter(chat_room=chat_room)[0:25]

    return render(
        request, "chat/chat_room.html", {"room": chat_room, "messages": messages}
    )
