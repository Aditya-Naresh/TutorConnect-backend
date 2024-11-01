from django.urls import path
from .views import (
    TutorListView,
    StudentListView,
    UserUpdateView,
    SubjectListView,
    CertificationListView,
)

urlpatterns = [
    path(
        "tutor-list/",
        TutorListView.as_view(),
        name="tutor-list-update",
    ),
    path(
        "tutor/approval/",
        TutorListView.as_view(),
        name="tutor-list-approval",
    ),
    path(
        "student-list/",
        StudentListView.as_view(),
        name="student-list-update",
    ),
    path(
        "update-user/<id>",
        UserUpdateView.as_view(),
        name="student-list-update-id",
    ),
    path(
        "subjects/<user_id>",
        SubjectListView.as_view(),
        name="subject-list",
    ),
    path(
        "certificates/<user_id>",
        CertificationListView.as_view(),
        name="certificate-list",
    ),
]
