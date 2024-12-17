from django.test import TestCase
from channels.testing import WebsocketCommunicator
from tutorconnect.asgi import application  # Replace with your ASGI application path
import json


class VideoCallConsumerTestCase(TestCase):
    async def test_video_call_consumer(self):
        # Set up WebSocket connection
        communicator = WebsocketCommunicator(application, "/ws/video/call/123/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send an "offer" message
        await communicator.send_json_to(
            {
                "action": "offer",
                "target_username": "user2",
                "offer": "SDP_OFFER_DATA",
            }
        )

        # Receive the forwarded "offer" message
        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {
                "type": "OFFER",
                "offer": "SDP_OFFER_DATA",
                "from": "123",
            },
        )

        # Close the WebSocket
        await communicator.disconnect()
