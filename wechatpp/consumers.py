import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from chatapp.models import Room, Message, User
from chatapp.sentiment import analyze_sentiment
from .utils import save_file

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.roomGroupName = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
    

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", "")  # Optional for file messages
        username = text_data_json["username"]
        room_name = text_data_json["room_name"]
        file_data = text_data_json.get("file")  # Base64 encoded file data (if present)
        file_name = text_data_json.get("file_name", None)  # Optional file name

        # If a file is sent, save the file and generate a URL
        if file_data and file_name:
            file_url = await self.save_and_get_file_url(file_data, file_name, username, room_name)
            sentiment_score = None  # Files do not have sentiment
        else:
            # Analyze sentiment for text messages
            sentiment_score = analyze_sentiment(message)
            file_url = None  # No file in this case
            await self.save_message(message, username, room_name)

        # Broadcast the message or file to the group
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "room_name": room_name,
                "sentiment": sentiment_score,  # Include sentiment score
                "file_name": file_name,
                "file_url": file_url,  # Include file URL if a file is sent
            }
        )

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        sentiment = event.get("sentiment", None)  # Optional sentiment for files
        file_name = event.get("file_name", None)  # Optional file name
        file_url = event.get("file_url", None)  # Optional file URL

        # Send message, file, and sentiment to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "sentiment": sentiment,  # Include sentiment if present
            "file_name": file_name,  # Include file name if present
            "file_url": file_url,  # Include file URL if present
        }))
    
    @sync_to_async
    def save_message(self, message, username, room_name):
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)
        Message.objects.create(user=user, room=room, content=message)

    @sync_to_async
    def save_and_get_file_url(self, file_data, file_name, username, room_name):
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)

        # Decode base64 file data
        decoded_file = base64.b64decode(file_data)

        # Save the file using the utility function
        uploaded_file = ContentFile(decoded_file, name=file_name)
        file_url = save_file(uploaded_file)  # Save the file and get its URL

        # Save the file info in the database
        message = Message.objects.create(user=user, room=room, file=uploaded_file)
        message.save()

        return file_url
