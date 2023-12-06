from django.urls import re_path as _

from . import views

urlpatterns = [
    _(
        r"^chat_rooms",
        views.chat_rooms,
        name="chat_rooms",
    ),
    _(
        r"^messages/(?P<slug>[\w-]+)$",
        views.messages,
        name="messages",
    ),
    
]
