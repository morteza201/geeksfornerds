# Generated by Django 5.1.5 on 2025-01-23 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_class_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='description',
            field=models.TextField(),
        ),
    ]
