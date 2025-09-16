from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length=50)
    monthly_quota = models.IntegerField(default=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class User(AbstractUser):
    phone = models.CharField(max_length=12, verbose_name='phone_number', unique=True)
    user_name = models.CharField(max_length=100)
    active_code = models.CharField(max_length=8, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return f'{self.phone} - {self.user_name}'
