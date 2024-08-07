# Generated by Django 5.0.6 on 2024-07-21 00:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0016_alter_user_joined_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 21, 8, 10, 58, 838276), help_text='Designates the joined date and time of the user.', verbose_name='Joined Date'),
        ),
    ]
