# Generated by Django 5.0.4 on 2024-05-25 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0012_post_validated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='depth',
            name='is_profound',
            field=models.BooleanField(default=False, help_text='Designates that the depth is profound.', verbose_name='Profound'),
        ),
    ]
