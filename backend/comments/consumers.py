import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the "comments" group
        await self.channel_layer.group_add("comments", self.channel_name)
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the "comments" group
        await self.channel_layer.group_discard("comments", self.channel_name)

    async def receive(self, text_data):
        # Broadcast received message to the group
        await self.channel_layer.group_send(
            "comments",
            {
                "type": "comment_message",
                "message": text_data,
            }
        )

    async def comment_message(self, event):
        # Send message to WebSocket client
        await self.send(text_data=event["message"])
