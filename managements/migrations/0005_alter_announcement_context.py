# Generated by Django 5.0.4 on 2024-06-25 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managements', '0004_alter_statustype_statustype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='context',
            field=models.TextField(blank=True, help_text='Designates the context of the announcement.', max_length=5000, null=True, verbose_name='Context'),
        ),
    ]