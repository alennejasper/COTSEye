# Generated by Django 5.0 on 2024-03-26 11:46

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, help_text='Designates the latitude of the post.', max_digits=9, verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=6, help_text='Designates the longitude of the post.', max_digits=9, verbose_name='Longitude')),
            ],
            options={
                'verbose_name': 'Coordinates',
                'verbose_name_plural': 'Coordinates',
                'db_table': 'reports_coordinates',
            },
        ),
        migrations.CreateModel(
            name='Depth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deep', models.BooleanField(default=False, help_text='Designates that the depth is deep.', verbose_name='Deep')),
                ('is_moderate', models.BooleanField(default=False, help_text='Designates that the depth is moderate.', verbose_name='Moderate')),
                ('is_shallow', models.BooleanField(default=False, help_text='Designates that the depth is shallow.', verbose_name='Shallow')),
            ],
            options={
                'verbose_name': 'Depth',
                'verbose_name_plural': 'Depths',
                'db_table': 'reports_depth',
            },
        ),
        migrations.CreateModel(
            name='PostPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_photo', models.ImageField(default='posts/default.png', help_text='Designates the photo of the post.', null=True, upload_to='posts', verbose_name='Post Photo')),
            ],
            options={
                'verbose_name': 'Post Photo',
                'verbose_name_plural': 'Posts Photos',
                'db_table': 'reports_post_photo',
            },
        ),
        migrations.CreateModel(
            name='PostStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=False, help_text='Designates that the post can be pinned into the contributors site.', verbose_name='Valid')),
                ('is_invalid', models.BooleanField(default=False, help_text='Designates that the post cannot be pinned into the contributors site.', verbose_name='Invalid')),
                ('is_uncertain', models.BooleanField(default=False, help_text='Designates that the post is under review to be pinned into the contributors site.', verbose_name='Uncertain')),
            ],
            options={
                'verbose_name': 'Post Status',
                'verbose_name_plural': 'Posts Status',
                'db_table': 'reports_post_status',
            },
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sunny', models.BooleanField(default=False, help_text='Designates that the weather is sunny.', verbose_name='Sunny')),
                ('is_cloudy', models.BooleanField(default=False, help_text='Designates that the weather is cloudy.', verbose_name='Cloudy')),
                ('is_windy', models.BooleanField(default=False, help_text='Designates that the weather is windy.', verbose_name='Windy')),
                ('is_rainy', models.BooleanField(default=False, help_text='Designates that the weather is rainy.', verbose_name='Rainy')),
                ('is_stormy', models.BooleanField(default=False, help_text='Designates that the weather is stormy.', verbose_name='Stormy')),
            ],
            options={
                'verbose_name': 'Weather',
                'verbose_name_plural': 'Weathers',
                'db_table': 'reports_weather',
            },
        ),
        migrations.CreateModel(
            name='PostObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(blank=True, help_text='Designates the size of the Crown-of-Thorns Starfish at the moment the post taken.', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Size / Centimeter')),
                ('density', models.IntegerField(blank=True, help_text='Designates the density of the Crown-of-Thorns Starfish at the moment the post taken.', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Density / Square Meter')),
                ('depth', models.ForeignKey(blank=True, help_text='Designates the foreign key of the Depth model.', null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.depth', verbose_name='Depth')),
                ('weather', models.ForeignKey(blank=True, help_text='Designates the foreign key of the Weather model.', null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.weather', verbose_name='Weather')),
            ],
            options={
                'verbose_name': 'Post Observation',
                'verbose_name_plural': 'Posts Observations',
                'db_table': 'reports_post_observation',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(help_text='Designates the description of the post.', max_length=1500, verbose_name='Description')),
                ('capture_date', models.DateField(default=datetime.datetime(2024, 3, 26, 19, 46, 34, 705502), help_text='Designates the capture date and time of the post.', verbose_name='Capture Date')),
                ('coordinates', models.ForeignKey(help_text='Designates the foreign key of the Coordinates model.', on_delete=django.db.models.deletion.CASCADE, to='reports.coordinates', verbose_name='Coordinates')),
                ('user', models.ForeignKey(help_text='Designates the foreign key of the User model.', on_delete=django.db.models.deletion.CASCADE, to='authentications.user', verbose_name='User')),
                ('post_observation', models.ForeignKey(blank=True, help_text='Designates the foreign key of the Post Observation model.', null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.postobservation', verbose_name='Post Observation')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'db_table': 'reports_post',
            },
        ),
        migrations.CreateModel(
            name='PostGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(help_text='Designates the foreign key of the Post model.', on_delete=django.db.models.deletion.CASCADE, to='reports.post', verbose_name='Post')),
                ('post_photos', models.ForeignKey(help_text='Designates the foreign key of the Post Photos model.', on_delete=django.db.models.deletion.CASCADE, to='reports.postphoto', verbose_name='Post Photo')),
            ],
            options={
                'verbose_name': 'Post Gallery',
                'verbose_name_plural': 'Posts Gallery',
                'db_table': 'reports_post_gallery',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='post_photos',
            field=models.ManyToManyField(blank=True, help_text='Designates the foreign key of the Post Photo model.', through='reports.PostGallery', to='reports.postphoto', verbose_name='Post Photos'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_status',
            field=models.ForeignKey(default=1, help_text='Designates the foreign key of the Post Status model.', on_delete=django.db.models.deletion.CASCADE, to='reports.poststatus', verbose_name='Post Status'),
        ),
    ]
