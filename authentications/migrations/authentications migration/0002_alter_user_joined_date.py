# Generated by Django 5.0.4 on 2024-05-14 06:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 14, 14, 56, 52, 863623), help_text='Designates the joined date and time of the user.', verbose_name='Joined Date'),
        ),
    ]
