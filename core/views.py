from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserCreateSerializer

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
