from django.urls import path
from . views import RegisterUserView
urlpatterns = [
    path("signup/", RegisterUserView.as_view(), name='register_user')
]
