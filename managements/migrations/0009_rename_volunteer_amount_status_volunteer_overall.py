# Generated by Django 5.0.4 on 2024-05-26 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managements', '0008_status_volunteer_amount_alter_status_caught_overall'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status',
            old_name='volunteer_amount',
            new_name='volunteer_overall',
        ),
    ]
