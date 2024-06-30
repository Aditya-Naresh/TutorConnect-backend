from django.urls import path
from .views import CreateTutorDatesView, TutorDatesListView, TimeSlotsListView

urlpatterns = [
    path('create-tutor-dates/', CreateTutorDatesView.as_view(), name='create-tutor-dates'),
    path('available-dates/<id>', TutorDatesListView.as_view(), name='tutor-dates'),
    path('timeSlots/<id>', TimeSlotsListView.as_view(), name='time-slots'),
]
