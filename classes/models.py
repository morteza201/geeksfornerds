from django.db import models
from accounts.models import CustomUser
from courses.models import Course
from django.utils import timezone

# Create your models here.
class Class(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    password = models.CharField(max_length=64)
    creator = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='created_classes')
    students = models.ManyToManyField(to=CustomUser, related_name='enrolled_classes', blank=True)
    courses = models.ManyToManyField(to=Course, related_name='classes_included', blank=True)
    created_at = models.DateField(auto_now_add=True)