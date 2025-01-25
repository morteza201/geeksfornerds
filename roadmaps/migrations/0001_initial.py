# Generated by Django 5.1.4 on 2024-12-20 09:48

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Roadmap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_roadmaps', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(blank=True, related_name='enrolled_roadmaps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roadmap_rates_submited', to=settings.AUTH_USER_MODEL)),
                ('roadmap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roadmap_rates', to='roadmaps.roadmap')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('replied_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='roadmaps.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roadmap_comments_writed', to=settings.AUTH_USER_MODEL)),
                ('roadmap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roadmap_comments', to='roadmaps.roadmap')),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('courses', models.ManyToManyField(blank=True, related_name='linked_to_steps', to='courses.course')),
                ('roadmap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='roadmaps.roadmap')),
            ],
        ),
    ]
