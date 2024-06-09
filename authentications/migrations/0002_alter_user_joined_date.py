# Generated by Django 5.0.4 on 2024-06-04 07:03

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
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 4, 15, 3, 17, 43730), help_text='Designates the joined date and time of the user.', verbose_name='Joined Date'),
        ),
    ]
