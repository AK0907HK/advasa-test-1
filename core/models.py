from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    available_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} profile"
