# Generated by Django 5.0.4 on 2024-06-21 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=7, help_text='Designates the pin latitude of the location.', max_digits=27, null=True, verbose_name='Pin Latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=7, help_text='Designates the pin longitude of the location.', max_digits=27, null=True, verbose_name='Pin Longitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='perimeters',
            field=models.TextField(blank=True, help_text='Designates the map perimeters of the location.', null=True, verbose_name='Map Perimeters'),
        ),
    ]