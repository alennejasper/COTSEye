# Generated by Django 5.0.6 on 2024-07-23 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managements', '0006_alter_barangay_barangay_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='intervention',
            options={'verbose_name': 'Activity', 'verbose_name_plural': 'Activities'},
        ),
    ]
