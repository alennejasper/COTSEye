# Generated by Django 5.0.4 on 2024-05-18 03:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0009_post_creation_date_alter_post_capture_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='read_date',
            field=models.DateTimeField(blank=True, help_text='Designates the date and time when the post was read.', null=True, verbose_name='Read Date'),
        ),
        migrations.AddField(
            model_name='post',
            name='read_status',
            field=models.BooleanField(default=False, help_text='Indicates whether the post has been read.', verbose_name='Read Status'),
        ),
        migrations.AlterField(
            model_name='post',
            name='capture_date',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='Designates the capture date and time of the post.', verbose_name='Capture Date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='Designates the creation date and time of the post.', verbose_name='Creation Date'),
        ),
    ]
