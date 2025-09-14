from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class OTPCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=16, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at >= timezone.now()
