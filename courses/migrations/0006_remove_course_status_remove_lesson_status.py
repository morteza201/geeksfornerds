# Generated by Django 5.1.5 on 2025-01-23 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_status_lesson_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='status',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='status',
        ),
    ]
