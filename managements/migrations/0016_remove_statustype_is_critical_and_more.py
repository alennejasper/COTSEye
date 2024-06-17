# Generated by Django 5.0.4 on 2024-06-16 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managements', '0015_intervention_creation_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statustype',
            name='is_critical',
        ),
        migrations.RemoveField(
            model_name='statustype',
            name='is_high',
        ),
        migrations.RemoveField(
            model_name='statustype',
            name='is_low',
        ),
        migrations.RemoveField(
            model_name='statustype',
            name='is_moderate',
        ),
        migrations.AddField(
            model_name='statustype',
            name='statustype',
            field=models.CharField(default=None, help_text='Designates the status type.', max_length=65, verbose_name='Status Level Type'),
        ),
    ]
