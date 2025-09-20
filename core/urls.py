from django.urls import path
from .views import UserCreateView
from .views import MeView
from .views import ApplicationCreateView

urlpatterns = [
    path("users/", UserCreateView.as_view(), name="user_create"),
    path("me/", MeView.as_view(), name="me"),
    path("applications/", ApplicationCreateView.as_view(), name="applications_create"),
]
