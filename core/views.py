from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserCreateSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.generic import TemplateView
from .serializers import ApplicationCreateSerializer
from .models import Application

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "id": u.id,
            "username": u.username,
            "available_amount": getattr(u, "profile", None).available_amount if hasattr(u, "profile") else 0,
        })

class LoginPageView(TemplateView):
    template_name = "login.html"

class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()

class LoginPageView(TemplateView):
    template_name = "login.html"       
    
class ApplyPageView(TemplateView):
    template_name = "apply.html"

class CompletePageView(TemplateView):
    template_name = "complete.html"   