# Generated by Django 5.0.4 on 2024-06-16 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0015_alter_depth_options_alter_size_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depth',
            name='is_deep',
        ),
        migrations.RemoveField(
            model_name='depth',
            name='is_moderate',
        ),
        migrations.RemoveField(
            model_name='depth',
            name='is_profound',
        ),
        migrations.RemoveField(
            model_name='depth',
            name='is_shallow',
        ),
        migrations.RemoveField(
            model_name='size',
            name='is_large',
        ),
        migrations.RemoveField(
            model_name='size',
            name='is_medium',
        ),
        migrations.RemoveField(
            model_name='size',
            name='is_small',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='is_cloudy',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='is_rainy',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='is_stormy',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='is_sunny',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='is_windy',
        ),
        migrations.AddField(
            model_name='depth',
            name='depth',
            field=models.CharField(help_text='Designates the depth.', max_length=65, null=True, verbose_name='Depth'),
        ),
        migrations.AddField(
            model_name='size',
            name='size',
            field=models.CharField(help_text='Designates the size.', max_length=65, null=True, verbose_name='Depth'),
        ),
        migrations.AddField(
            model_name='weather',
            name='weather',
            field=models.CharField(help_text='Designates the weather.', max_length=65, null=True, verbose_name='Weather'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(help_text='Designates the description of the post.', max_length=255, verbose_name='Description'),
        ),
    ]
