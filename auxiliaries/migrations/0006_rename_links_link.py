# Generated by Django 5.0.4 on 2024-06-04 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliaries', '0005_rename_link_links'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Links',
            new_name='Link',
        ),
    ]
