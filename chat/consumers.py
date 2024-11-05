import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRooms, Messages

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.request_user = self.scope["user"]
            if self.request_user.is_authenticated:
                self.chat_with_user = self.scope["url_route"]["kwargs"]["id"]
                try:
                    self.chat_with_user = int(self.chat_with_user)
                except ValueError:
                    print(
                        f"Error: {self.chat_with_user} is not a valid integer",
                    )
                    await self.close()
                user_ids = [
                    int(self.request_user.id),
                    int(self.chat_with_user),
                ]
                user_ids = sorted(user_ids)
                if user_ids[0] == user_ids[1]:
                    print(user_ids)
                    print("Tried to create a chat room with single user")
                    await self.close()

                self.room_group_name = f"chat_{user_ids[0]}-{user_ids[1]}"

                await self.channel_layer.group_add(
                    self.room_group_name, self.channel_name
                )
                self.chat_room = await self.get_or_create_chat_room()

                # Fetch and send previous messages
                messages = await self.get_messages()

                await self.accept()
                await self.send(text_data=messages)

            else:
                await self.close()
        except Exception as e:
            print(f"Error in connect: {str(e)}")
            await self.close()

    async def disconnect(self, code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        except Exception as e:
            print(f"Error in disconnect: {str(e)}")

    @database_sync_to_async
    def get_or_create_chat_room(self):
        user1 = self.request_user
        user2 = User.objects.get(id=int(self.chat_with_user))
        user_ids = sorted([user1.id, user2.id])

        chat_room, created = ChatRooms.objects.get_or_create(
            user1_id=user_ids[0],
            user2_id=user_ids[1],
            defaults={"user1_id": user_ids[0], "user2_id": user_ids[1]},
        )
        return chat_room, created

    @database_sync_to_async
    def save_message(self, message_content):
        chat_room = self.chat_room[0]
        message = Messages.objects.create(
            chat_room=chat_room,
            user=self.request_user,
            content=message_content,
            seen=False,
        )

        return {
            "message_id": message.id,
            "timestamp": message.timestamp.isoformat(),  # Return the timestamp
            "seen": message.seen,
        }

    @database_sync_to_async
    def get_messages(self):
        chat_room = self.chat_room[0]
        messages = Messages.objects.filter(
            chat_room=chat_room,
        ).order_by("timestamp")
        message_list = [
            {
                "id": message.id,
                "content": message.content,
                "user": message.user.id,
                "username": message.user.get_full_name(),
                "timestamp": message.timestamp.isoformat(),
                "seen": message.seen,
            }
            for message in messages
        ]
        json_messages = json.dumps(
            {
                "type": "history",
                "messages": message_list,
            }
        )

        return json_messages

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")

            if message:
                result = await self.save_message(message)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message_id": result["message_id"],
                        "content": message,
                        "username": self.request_user.get_full_name(),
                        "user": self.request_user.id,
                        "timestamp": result["timestamp"],
                        "seen": result["seen"],
                    },
                )

        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "message_id": event["message_id"],
                    "content": event["content"],
                    "username": event["username"],
                    "user": event["user"],
                    "timestamp": event["timestamp"],
                    "seen": event["seen"],
                }
            )
        )
