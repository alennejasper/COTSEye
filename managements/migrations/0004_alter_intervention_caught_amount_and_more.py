# Generated by Django 5.0.4 on 2024-05-07 11:20

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managements', '0003_alter_intervention_intervention_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervention',
            name='caught_amount',
            field=models.IntegerField(blank=True, help_text='Designates the amount of the caught Crown-of-Thorns Starfish at the moment the intervention took place.', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Caught Amount'),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='intervention_date',
            field=models.DateField(default=datetime.date(2024, 5, 7), help_text='Designates the date of the intervention.', verbose_name='Intervention Date'),
        ),
        migrations.AlterField(
            model_name='status',
            name='onset_date',
            field=models.DateField(default=datetime.date(2024, 5, 7), help_text='Designates the onset date of the outbreak status.', verbose_name='Onset Date'),
        ),
    ]
