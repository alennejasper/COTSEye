# Generated by Django 5.0.6 on 2024-06-08 08:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0035_alter_user_joined_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 8, 16, 16, 56, 338589), help_text='Designates the joined date and time of the user.', verbose_name='Joined Date'),
        ),
    ]
