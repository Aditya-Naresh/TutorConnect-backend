from django.urls import path
from .views import UpdateNotificationView

urlpatterns = [
    path("update/<id>", UpdateNotificationView.as_view()),
]
