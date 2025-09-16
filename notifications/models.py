import uuid

from django.db import models
import secrets, hashlib
from users.models import User


# Create your models here.




class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    hashed_key = models.CharField(max_length=64)
    prefix = models.CharField(max_length=8)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def generate_key():
        raw = secrets.token_urlsafe(32)
        prefix = raw.split('-')[0]
        hashed = hashlib.sha256(raw.encode()).hexdigest()
        return raw, prefix, hashed

    def __str__(self):
        return f'{self.user.user_name} - {self.name}'


class Notification(models.Model):
    STATUS_CHOICES = [('queued', 'queued'), ('sent', 'sent'), ('failed', 'failed')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.ForeignKey(APIKey, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=10, choices=[('email', 'email'), ('sms', 'sms')])
    to = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    metadata = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='queued')
    provider_response = models.JSONField(null=True, blank=True)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.user_name} - {self.id} - {self.status}'
