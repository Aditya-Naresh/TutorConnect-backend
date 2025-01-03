import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import get_unread_notifications


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.request_user = self.scope["user"]
        self.group_name = f"notifications_{self.request_user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()
        await self.send_unread_notifications()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )
        except Exception as e:
            print(f"Error in disconnect: {str(e)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "notification_message",
                    "message": message,
                },
            )
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            await self.send(
                text_data=json.dumps(
                    {"error": "Invalid JSON format"},
                )
            )
        except Exception as e:
            print(f"Error processing message: {e}")
            await self.send(
                text_data=json.dumps(
                    {"error": "An error occurred while processing the message"}
                )
            )

    async def notification_message(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "notification_message",
                    "message": message,
                }
            )
        )

    async def send_unread_notifications(self):
        notifications = await get_unread_notifications(self.request_user)
        if notifications:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "unread_notifications",
                    "notifications": notifications,
                },
            )

    async def unread_notifications(self, event):
        notifications = event["notifications"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "unread_notifications",
                    "notifications": notifications,
                }
            )
        )
