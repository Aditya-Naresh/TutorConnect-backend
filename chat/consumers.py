import base64
import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import ChatRooms, Messages
from django.db.models import Q, Count, Value
from django.db.models.functions import Coalesce
from .serializers import ChatroomSerializer
import uuid
from django.core.files.base import ContentFile

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope["user"]
            if not self.user.is_authenticated:
                await self.close()
                return

            try:
                self.chat_partner_id = int(self.scope["url_route"]["kwargs"]["id"])
            except (ValueError, KeyError):
                await self.close()
                return

            if self.user.id == self.chat_partner_id:
                await self.close()
                return

            user_ids = sorted([self.user.id, self.chat_partner_id])
            self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )

            self.chat_room = await self.get_or_create_chat_room()

            await self.accept()
            # Message history
            await self.send_message_history()

        except Exception as e:
            print(f"Connection error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        except Exception as e:
            print(f"Disconnect error: {e}")

    @database_sync_to_async
    def get_or_create_chat_room(self):
        """Get or create a chat room between two users"""
        user_ids = sorted([self.user.id, self.chat_partner_id])
        chat_room, _ = ChatRooms.objects.get_or_create(
            user1_id=user_ids[0], user2_id=user_ids[1]
        )
        return chat_room

    @database_sync_to_async
    def save_message(self, content, attachment_data=None):
        """Save message with optional attachment"""
        try:
            # Create message
            message = Messages.objects.create(
                chat_room=self.chat_room,
                user=self.user,
                content=content or "",
                seen=False,
            )

            if attachment_data:
                try:
                    file_content = base64.b64decode(
                        attachment_data["fileContent"],
                    )
                    file_obj = ContentFile(file_content)

                    filename = f"{uuid.uuid4()}_{attachment_data['fileName']}"

                    message.attachment.save(filename, file_obj)
                    attachment_url = message.attachment.url
                except Exception as e:
                    print(f"Attachment save error: {e}")
                    attachment_url = None
            else:
                attachment_url = None

            return {
                "id": message.id,
                "content": message.content,
                "attachment": attachment_url,
                "timestamp": message.timestamp.isoformat(),
                "user": message.user.id,
                "username": message.user.get_full_name(),
                "seen": message.seen,
            }
        except Exception as e:
            print(f"Message save error: {e}")
            return None

    async def send_message_history(self):
        """Fetch and send message history"""
        try:

            messages = await self.get_messages()

            await self.mark_messages_as_seen()
            # Send history
            await self.send(
                text_data=json.dumps({"type": "history", "messages": messages})
            )
        except Exception as e:
            print(f"History send error: {e}")

    @database_sync_to_async
    def mark_messages_as_seen(self):
        """Mark unread messages from chat partner as seen"""
        Messages.objects.filter(chat_room=self.chat_room, seen=False).exclude(
            user=self.user
        ).update(seen=True)

    @database_sync_to_async
    def get_messages(self):
        """Retrieve messages for this chat room"""
        messages = Messages.objects.filter(chat_room=self.chat_room).order_by(
            "timestamp"
        )

        return [
            {
                "id": message.id,
                "content": message.content,
                "attachment": message.attachment.url if message.attachment else None,
                "user": message.user.id,
                "username": message.user.get_full_name(),
                "timestamp": message.timestamp.isoformat(),
                "seen": message.seen,
            }
            for message in messages
        ]

    async def receive(self, text_data):
        """Handle incoming messages"""
        try:
            data = json.loads(text_data)

            # Extract message and attachment
            message_content = data.get("message", "").strip()
            attachment_data = data.get("attachment")

            # Validate message or attachment
            if not message_content and not attachment_data:
                return

            # Save message
            message_data = await self.save_message(
                content=message_content, attachment_data=attachment_data
            )

            if message_data:
                # Broadcast message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        **message_data,
                    },
                )

                # Notify recipient about new message
                await self.notify_recipient()

        except Exception as e:
            print(f"Receive error: {e}")
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def chat_message(self, event):
        """Send message to WebSocket"""
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    **event,
                }
            )
        )

    async def notify_recipient(self):
        """Send notification to recipient about new message"""
        recipient_group_name = f"chatNotification_{self.chat_partner_id}"
        await self.channel_layer.group_send(
            recipient_group_name, {"type": "update_unseen_count"}
        )


class ChatRoomConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.request_user = self.scope["user"]
            self.room_group_name = f"chatNotification_{self.request_user.id}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )

            await self.accept()
            await self.fetch_updates()

        except Exception as e:
            print("Error in connect:", str(e))
            await self.close()

    async def disconnect(self, code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        except Exception as e:
            print(f"Error in disconnect: {str(e)}")

    async def send_chat_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def update_unseen_count(self, event):
        await self.fetch_updates()

    @sync_to_async
    def get_unseen_counts(self):
        users = ChatRooms.objects.filter(
            Q(user1=self.request_user) | Q(user2=self.request_user)
        ).annotate(
            unseen_count=Coalesce(
                Count(
                    "message",
                    filter=Q(message__seen=False)
                    & ~Q(
                        message__user=self.request_user,
                    ),
                ),
                Value(0),
            )
        )

        serializer = ChatroomSerializer(users, many=True)
        return serializer.data

    async def fetch_updates(self):
        data = await self.get_unseen_counts()
        unseen_contact = sum(1 for contact in data if contact["unseen_count"])
        await self.send_chat_update(
            {
                "data": data,
                "message_notification": f"{unseen_contact}",
            }
        )
