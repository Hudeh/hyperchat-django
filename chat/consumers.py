import json
import base64
from django.core.files.base import ContentFile
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    global file_url

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        attachment = data.get("attachment")
        message = data.get("message")
        sender = data.get("username")
        chat_room = data.get("chat_room")

        msg = await self.save_message(sender, chat_room, message, attachment)
        file_url = msg.attachment.url if msg.attachment else None

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
                "attachment": file_url,
                "timestamp": msg.timestamp,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        attachment = event["attachment"]

        await self.send(
            text_data=json.dumps(
                {"message": message, "username": sender, "attachment": attachment}
            )
        )

    @sync_to_async
    def save_message(self, sender, chat_room, message, attachment):
        sender = User.objects.get(username=sender)
        room = ChatRoom.objects.get(slug=chat_room)

        msg = Message.objects.create(sender=sender, chat_room=room, message=message)
        try:
            if attachment:
                ext = attachment.split(",")[0].split("/")[1].split(";")[0]
                file_content = base64.b64decode(attachment.split(",")[1])
                file_content_file = ContentFile(file_content)
                msg.attachment.save(
                    f"chat_file.{ext}",
                    file_content_file,
                    save=True,
                )
            return msg
        except:
            pass
