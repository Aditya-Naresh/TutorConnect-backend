from django.urls import path
from .views import *

urlpatterns = [
    path('tutor_timeslots/', TutorTimeSlotView.as_view(), name='tutor_timeslot'),
    path('<id>', RetrieveUpdateTimeSlotView.as_view(), name='timeslot-id'),
]
