# Generated by Django 5.0.4 on 2024-06-04 07:02

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentications', '0001_initial'),
        ('managements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Designates the title of the resource file.', max_length=150, verbose_name='Title')),
                ('resource_file', models.FileField(help_text='Designates the file of the resource.', upload_to='resources', verbose_name='Resource File')),
                ('release_date', models.DateTimeField(default=datetime.datetime.now, help_text='Designates the release date and time of the resource file.', verbose_name='Release Date')),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
                'db_table': 'auxiliaries_file',
            },
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(help_text='Designates the question of the inquiry.', max_length=150, verbose_name='Question')),
                ('answer', models.TextField(help_text='Designates the answer of the inquiry.', max_length=5000, verbose_name='Answer')),
            ],
            options={
                'verbose_name': 'Inquiry',
                'verbose_name_plural': 'Inquiries',
                'db_table': 'auxiliaries_inquiry',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Designates the title of the resource link.', max_length=150, verbose_name='Title')),
                ('resource_link', models.CharField(help_text='Designates the link of the resource.', max_length=2050, verbose_name='Resource Link')),
                ('release_date', models.DateTimeField(default=datetime.datetime.now, help_text='Designates the release date and time of the resource link.', verbose_name='Release Date')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
                'db_table': 'auxiliaries_link',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(help_text='Designates the name of the author.', max_length=150, verbose_name='Author')),
                ('title', models.CharField(help_text='Designates the title of the resource.', max_length=150, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
                'db_table': 'auxiliaries_resource',
            },
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hosting_agency', models.CharField(blank=True, help_text='Designates the name of the hosting agency.', max_length=150, null=True, verbose_name='Hosting Agency')),
                ('title', models.CharField(help_text='Designates the title of the announcement.', max_length=150, verbose_name='Title')),
                ('context', models.TextField(help_text='Designates the context of the announcement.', max_length=5000, verbose_name='Context')),
                ('release_date', models.DateTimeField(default=datetime.datetime.now, help_text='Designates the release date and time of the announcement.', verbose_name='Release Date')),
                ('announcement_photo', models.ImageField(default='announcements/default.png', help_text='Designates the photo of the announcement.', null=True, upload_to='announcements', verbose_name='Announcement Photo')),
                ('location', models.ForeignKey(blank=True, help_text='Designates the foreign key of the Location model.', null=True, on_delete=django.db.models.deletion.CASCADE, to='managements.location', verbose_name='Location')),
                ('user', models.ForeignKey(help_text='Designates the foreign key of the User model.', on_delete=django.db.models.deletion.CASCADE, to='authentications.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcements',
                'db_table': 'auxiliaries_announcement',
            },
        ),
    ]
