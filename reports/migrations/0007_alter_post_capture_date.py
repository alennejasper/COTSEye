# Generated by Django 5.0.4 on 2024-05-14 07:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_alter_post_capture_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='capture_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 14, 15, 17, 11, 141176), help_text='Designates the capture date and time of the post.', verbose_name='Capture Date'),
        ),
    ]
