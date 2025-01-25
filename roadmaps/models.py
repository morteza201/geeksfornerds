from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser
from courses.models import Course
from django.utils import timezone

# Create your models here.
class Roadmap(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='created_roadmaps')
    students = models.ManyToManyField(to=CustomUser, related_name='enrolled_roadmaps', blank=True)
    created_at = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)

    def get_rating(self):
        rates = Rate.objects.filter(roadmap=self.id)
        s = sum(c.rating for c in rates)
        c = rates.count()
        return round(s / c, 1) if c > 0 else 0  

class Step(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    roadmap = models.ForeignKey(to=Roadmap, on_delete=models.CASCADE, related_name='steps')
    courses = models.ManyToManyField(to=Course, related_name='linked_to_steps', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    text = models.TextField()
    creator = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='roadmap_comments_writed')
    roadmap = models.ForeignKey(to=Roadmap, on_delete=models.CASCADE, related_name='roadmap_comments')
    replied_comment = models.ForeignKey(to="self", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Rate(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    creator = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='roadmap_rates_submited')
    roadmap = models.ForeignKey(to=Roadmap, on_delete=models.CASCADE, related_name='roadmap_rates')
    created_at = models.DateTimeField(auto_now_add=True)