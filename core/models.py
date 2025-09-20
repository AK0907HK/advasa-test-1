from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    available_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} profile"

class Application(models.Model):
    STATUS_SUBMITTED = "SUBMITTED"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    amount = models.IntegerField()
    status = models.CharField(max_length=32, default=STATUS_SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "-created_at"]),  
        ]

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"