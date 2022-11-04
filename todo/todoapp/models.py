from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uid = models.TextField(null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.BooleanField(default=False)
    status = models.CharField(max_length=20)
