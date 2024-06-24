from django.urls import path
from . views import TutorListView, StudentListView, UserUpdateView
urlpatterns = [
    path('tutor-list/', TutorListView.as_view(), name='tutor-list-update' ),
    path('student-list/', StudentListView.as_view(), name='student-list-update' ),
    path('update-user/<id>', UserUpdateView.as_view(), name='student-list-update-id' ),
]
