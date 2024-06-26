# Generated by Django 5.0.4 on 2024-06-02 07:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0021_alter_user_joined_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 2, 15, 2, 41, 821792), help_text='Designates the joined date and time of the user.', verbose_name='Joined Date'),
        ),
    ]
