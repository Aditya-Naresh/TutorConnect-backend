from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import json
from asgiref.sync import sync_to_async
from timeslots.models import TimeSlots
from accounts.models import User


class AnalyticsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.role != User.Role.ADMIN:
            await self.disconnect()

        self.group_name = "analytics_group"
        try:
            self.channel_layer = get_channel_layer()

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name,
            )

            await self.accept()

            initial_data = await self.get_analytics_data()
            print("Initial Data", initial_data)
            await self.send(text_data=json.dumps(initial_data))

        except Exception as e:
            print(f"Connection error: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )
        except Exception as e:
            print(f"Disconnect error: {str(e)}")

    async def send_analytics_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def receive(self, text_data):
        pass

    @staticmethod
    async def get_analytics_data():
        total_users = await sync_to_async(User.objects.count)()
        total_tutors = await sync_to_async(
            User.objects.filter(role=User.Role.TUTOR).count
        )()
        total_students = await sync_to_async(
            User.objects.filter(role=User.Role.STUDENT).count
        )()
        ongoing_sessions = await sync_to_async(
            TimeSlots.objects.filter(status=TimeSlots.Status.ONGOING).count
        )()
        completed_sessions = await sync_to_async(
            TimeSlots.objects.filter(status=TimeSlots.Status.COMPLETED).count
        )()

        return {
            "totalUsers": total_users,
            "totalTutors": total_tutors,
            "totalStudents": total_students,
            "ongoingSessions": ongoing_sessions,
            "completedSessions": completed_sessions,
        }

    @classmethod
    async def broadcast_analytics(cls):
        try:
            channel_layer = get_channel_layer()
            analytics_data = await cls.get_analytics_data()

            users = await sync_to_async(User.objects.filter(role=User.Role.ADMIN))
            async for user in users:
                group_name = "analytics_group"
                await channel_layer.group_send(
                    group_name,
                    {
                        "type": "send_analytics_update",
                        "data": analytics_data,
                    },
                )
                print(f"Broadcastin to group: {group_name}")
        except Exception as e:
            print(f"Broadcast error: {str(e)}")
