from channels.db import database_sync_to_async
from timeslots.models import TimeSlots
from .serializers import TimeSlotSerializer


@database_sync_to_async
def get_time_slot(id):
    time_slot = TimeSlots.objects.get(id=id)
    time_slot_serializer = TimeSlotSerializer(
        time_slot,
    )
    return time_slot_serializer.data
