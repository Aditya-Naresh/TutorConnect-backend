from django.urls import path
from .views import *

urlpatterns = [
    path('tutor_timeslots/', TutorTimeSlotView.as_view(), name='tutor_timeslot'),
    path('student_timeslots/', StudentTimeSlotView.as_view(), name='student_timeslot'),
    path('<id>', RetrieveUpdateTimeSlotView.as_view(), name='timeslot-id'),
    path('tutor-list/', TutorListView.as_view(), name='tutor-list'),
    path('tutor-list/<id>', TutorListView.as_view(), name='tutor-list-id'),
    path('tuition-request/', TuitionRequestListCreateView.as_view(), name='tuition-request'),
    path('tuition-request/<id>', TuitionRequestRetrieveUpdateView.as_view(), name='tuition-request-id'),
    path('tutor_timeslots/<int:tutor_id>/', TutorTimeSlotsListView.as_view(), name='tutor_timeslots'),
    path('create-timeslots/', CreateTimeSlotsView.as_view(), name='create-timeslots')
]
