from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

# Create your models here.
class Animation(models.Model):
    title = models.CharField(max_length=255)
    src = models.TextField()
    creator = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='animation_created')
    created_at = models.DateField(auto_now_add=True)