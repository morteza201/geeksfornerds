# Generated by Django 5.1.5 on 2025-01-23 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roadmaps', '0005_roadmap_status_step_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roadmap',
            name='status',
        ),
        migrations.RemoveField(
            model_name='step',
            name='status',
        ),
    ]
