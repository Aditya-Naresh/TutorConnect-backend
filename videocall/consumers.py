from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from django.conf import settings


class NotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.userid = self.user.id
        self.group_name = f"notify_{self.userid}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        return await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        print(data)

        if action == "call_request":
            target_userid = data.get("target_user")
            self.timeslot = data.get("timeSlot")
            print("timeslot: ", self.timeslot)
            if self.userid != target_userid:
                profile_picture = await self.get_profile_picture(self.user)
                await self.channel_layer.group_send(
                    f"notify_{target_userid}",
                    {
                        "type": "send_call_request",
                        "from": self.userid,
                        "profile_picture": profile_picture,
                        "timeSlot": self.timeslot,
                    },
                )
        elif action == "accept_call":
            print("accepting call")
            target_userid = data.get("target_user")
            timeslot = data.get("timeSlot")
            if target_userid:
                await self.channel_layer.group_send(
                    f"notify_{target_userid}",
                    {
                        "type": "send_call_accept",
                        "from": self.userid,
                        "timeSlot": timeslot,
                    },
                )
        elif action == "reject":
            target_userid = data.get("target_user")
            print("rejected_by:", self.userid)
            await self.channel_layer.group_send(
                f"notify_{target_userid}",
                {
                    "type": "send_call_end",
                    "from": self.userid,
                },
            )
        elif action == "abandon_call":
            target_userid = data.get("target_user")
            print(target_userid)
            await self.channel_layer.group_send(
                f"notify_{target_userid}",
                {
                    "type": "send_call_abandoned",
                    "from": self.userid,
                },
            )
        elif action == "offer":
            target_userid = data.get("target_user")
            print(target_userid)
            offer = data.get("offer")
            await self.channel_layer.group_send(
                f"notify_{target_userid}",
                {
                    "type": "send_offer",
                    "from": self.userid,
                    "offer": offer,
                },
            )
        elif action == "answer":
            target_userid = data.get("target_user")
            answer = data.get("answer")
            await self.channel_layer.group_send(
                f"notify_{target_userid}",
                {
                    "type": "send_answer",
                    "from": self.userid,
                    "answer": answer,
                },
            )
        elif action == "ice_candidate":
            target_userid = data.get("target_user")
            candidate = data.get("candidate")
            await self.channel_layer.group_send(
                f"notify_{target_userid}",
                {
                    "type": "send_ice_candidate",
                    "from": self.userid,
                    "candidate": candidate,
                },
            )

    async def send_call_request(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "CALL_REQUEST",
                    "from": event["from"],
                    "profile_picture": event.get("profile_picture"),
                    "timeSlot": event["timeSlot"],
                }
            )
        )

    async def send_call_accept(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "CALL_ACCEPTED",
                    "from": event["from"],
                    "timeSlot": event["timeSlot"],
                }
            )
        )

    async def send_call_end(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "CALL_REJECTED",
                    "from": event["from"],
                }
            )
        )

    async def send_call_abandoned(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "CALL_ABANDONED",
                    "from": event["from"],
                }
            )
        )

    @sync_to_async
    def get_profile_picture(self, user):
        if user.profile_pic:
            return f"{user.profile_pic.url}"
        return f"{settings.MEDIA_URL}profile_pictures/default.jpg"

    async def send_offer(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "OFFER",
                    "from": event["from"],
                    "offer": event["offer"],
                }
            )
        )

    async def send_ice_candidate(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "ICE_CANDIDATE",
                    "from": event["from"],
                    "candidate": event["candidate"],
                }
            )
        )


class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.userid = self.scope["url_route"]["kwargs"]["userid"]
        self.room_group_name = f"video_call_{self.userid}"
        self.target_user = None
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
        print(f"WebSocket connection accepted for user: {self.userid}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

        if self.target_user:
            await self.forward_to_target(
                self.target_user,
                {
                    "type": "END_CALL",
                    "from": self.userid,
                },
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        print(data)

        if action == "offer":
            self.target_user = data.get("target_user")
            await self.forward_to_target(
                self.target_user,
                {
                    "type": "OFFER",
                    "offer": data["offer"],
                    "from": self.userid,
                },
            )

        elif action == "answer":
            self.target_user = data.get("target_user")
            await self.forward_to_target(
                self.target_user,
                {
                    "type": "ANSWER",
                    "answer": data["answer"],
                    "from": self.userid,
                },
            )

        elif action == "ice_candidate":
            target_user = data.get("target_user")
            await self.forward_to_target(
                target_user,
                {
                    "type": "ICE_CANDIDATE",
                    "candidate": data["candidate"],
                    "from": self.userid,
                },
            )

        elif action == "end_call":
            target_user = data.get("target_user")
            await self.forward_to_target(
                target_user,
                {
                    "type": "END_CALL",
                    "from": self.userid,
                },
            )

    async def forward_to_target(self, target_user, message):
        target_group_name = f"video_call_{target_user}"
        await self.channel_layer.group_send(
            target_group_name,
            {
                "type": "send_sdp_message",
                "message": message,
            },
        )

    async def send_sdp_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))
