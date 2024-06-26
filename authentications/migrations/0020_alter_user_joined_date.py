# Generated by Django 5.0.4 on 2024-05-29 09:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0019_alter_user_joined_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 17, 11, 48, 405898), help_text='Designates the joined date and time of the user.', verbose_name='Joined Date'),
        ),
    ]
