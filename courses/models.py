from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser
from animations.models import Animation
from django.utils import timezone

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='created_courses')
    students = models.ManyToManyField(to=CustomUser, blank=True, related_name='enrolled_courses')
    created_at = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)

    def get_rating(self):
        rates = Rate.objects.filter(course=self.id)
        s = sum(c.rating for c in rates)
        c = rates.count()
        return round(s / c, 1) if c > 0 else 0

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='lessons')
    animations = models.ManyToManyField(to=Animation, related_name='animations_used', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    text = models.TextField()
    creator = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='course_comments_writed')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='comments')
    replied_comment = models.ForeignKey(to="self", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Rate(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    creator = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='course_rates_submited')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='rates')
    created_at = models.DateTimeField(auto_now_add=True)