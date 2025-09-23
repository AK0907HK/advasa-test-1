from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import UserProfile, Application

User = get_user_model()

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "available_amount")
    search_fields = ("user__username", "user__email")
    list_select_related = ("user",)
    ordering = ("id",)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "status", "created_at")
    search_fields = ("user__username",)
    list_filter = ("status",)
    date_hierarchy = "created_at"
    list_select_related = ("user",)
    ordering = ("-created_at",)
