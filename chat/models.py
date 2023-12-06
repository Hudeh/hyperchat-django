import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

def get_upload_path(instance, filename):
    # Determine the upload path based on the file type
    if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
        return os.path.join("media", "picture", filename)
    elif filename.endswith((".mp4", ".avi", ".mov")):
        return os.path.join("media", "video", filename)
    else:
        return os.path.join("media", "other", filename)


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    max_members = models.IntegerField(default=1)
    slug = models.SlugField(unique=True)
    members = models.ManyToManyField(
        User, related_name="chat_rooms"
    )


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, related_name="user", on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ("timestamp",)
