from django.urls import path
from .views import CreateTutorDatesView, TutorDatesListView, TimeSlotsListView, TutorListView, TuitionRequestListCreateView, TuitionRequestRetrieveUpdateView, TimeSlotRetrieveUpdateView

urlpatterns = [
    path('create-tutor-dates/', CreateTutorDatesView.as_view(), name='create-tutor-dates'),
    path('available-dates/<id>', TutorDatesListView.as_view(), name='tutor-dates'),
    path('timeSlots/<id>', TimeSlotsListView.as_view(), name='time-slots'),
    path('BooktimeSlots/<id>', TimeSlotRetrieveUpdateView.as_view(), name='time-slots-booking'),
    path('tutor-list/', TutorListView.as_view(), name='tutor-list'),
    path('tuition-request/', TuitionRequestListCreateView.as_view(), name='tuition-request'),
    path('tuition-request/<id>', TuitionRequestRetrieveUpdateView.as_view(), name='tuition-request-id'),
]
