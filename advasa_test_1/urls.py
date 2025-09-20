from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('core.urls')),
]

from django.views.generic import TemplateView
urlpatterns += [
    path('login/', TemplateView.as_view(template_name='login.html')),
    path('apply/', TemplateView.as_view(template_name='apply.html')),
    path('complete/', TemplateView.as_view(template_name='complete.html')),
    path('history/', TemplateView.as_view(template_name='history.html')),
]
