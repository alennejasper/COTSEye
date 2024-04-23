# Generated by Django 5.0.4 on 2024-04-16 05:15

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that the user has all permissions.', verbose_name='Administrator')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into the officers site or not.', verbose_name='Officer')),
                ('is_contributor', models.BooleanField(default=False, help_text='Designates whether the user can log into the contributors site or not.', verbose_name='Contributor')),
            ],
            options={
                'verbose_name': 'User Type',
                'verbose_name_plural': 'User Types',
                'db_table': 'auth_user_type',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='Designates the name of the user.', max_length=150, unique=True, verbose_name='Username')),
                ('password', models.CharField(help_text='Designates the password of the user.', max_length=150, verbose_name='Password')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether the user should be considered active or not.', verbose_name='Active Status')),
                ('last_login', models.DateTimeField(default=datetime.datetime.now, help_text='Designates the last login date and time of the user.', verbose_name='Last Signin')),
                ('groups', models.ManyToManyField(help_text='Designates the foreign key of the Group model.', null=True, to='auth.group', verbose_name='Groups')),
                ('user_permissions', models.ManyToManyField(help_text='Designates the foreign key of the Permission model.', null=True, to='auth.permission', verbose_name='User Permissions')),
                ('usertype', models.ForeignKey(help_text='Designates the foreign key of the User Type model.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentications.usertype', verbose_name='User Type')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'db_table': 'auth_account',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Designates the first name of the user.', max_length=65, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(help_text='Designates the last name of the user.', max_length=65, null=True, verbose_name='Last Name')),
                ('email', models.EmailField(help_text='Designates the email of the user.', max_length=65, null=True, verbose_name='Email')),
                ('phone_number', models.IntegerField(blank=True, help_text='Designates the phone number of the user.', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Phone Number')),
                ('profile_photo', models.ImageField(default='profiles/default.png', help_text='Designates the profile photo of the user.', null=True, upload_to='profiles', verbose_name='Profile Photo')),
                ('joined_date', models.DateTimeField(default=datetime.datetime(2024, 4, 16, 13, 15, 6, 537401), help_text='Designates the joined date and time of the user.', verbose_name='Joined Date')),
                ('account', models.OneToOneField(help_text='Designates the foreign key of the Account model.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Account')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'localaccount_user',
            },
        ),
    ]
