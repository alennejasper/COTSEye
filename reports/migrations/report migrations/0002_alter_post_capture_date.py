# Generated by Django 5.0.4 on 2024-05-14 06:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='capture_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 14, 14, 56, 52, 879244), help_text='Designates the capture date and time of the post.', verbose_name='Capture Date'),
        ),
    ]
