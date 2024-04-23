from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.contrib.sites.models import Site
from django.utils.html import mark_safe
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp

import datetime


# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, username, password, **other_fields):
        username = username

        user = self.model(username = username, **other_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, username, password, **other_fields):
        username = "cotseye/" + username

        usertype, created = UserType.objects.get_or_create(is_superuser = True)

        if created:
            account = self.create_user(username, password, usertype = usertype, **other_fields)
        
        else:
            account = self.create_user(username, password, usertype = usertype, **other_fields)

        user = User.objects.create(account = account)

        return usertype, account, user


class UserType(models.Model):
    is_superuser = models.BooleanField(default = False, help_text = "Designates that the user has all permissions.", verbose_name = "Administrator")
    is_staff = models.BooleanField(default = False, help_text = "Designates whether the user can log into the officers site or not.", verbose_name = "Officer")
    is_contributor = models.BooleanField(default = False, help_text = "Designates whether the user can log into the contributors site or not.", verbose_name = "Contributor")

    class Meta:
        db_table = "auth_user_type"
        verbose_name = "User Type"
        verbose_name_plural = "User Types"

    def __str__(self):
        if self.is_superuser == True:
            return "Administrator"
        
        elif self.is_staff == True:
            return "Officer"

        elif self.is_contributor == True:
            return "Contributor"
        

class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 150, unique = True, help_text = "Designates the name of the user.", verbose_name = "Username")
    password = models.CharField(max_length = 150, help_text = "Designates the password of the user.", verbose_name = "Password")
    usertype = models.ForeignKey(UserType, on_delete = models.SET_NULL, null = True, help_text = "Designates the foreign key of the User Type model.", verbose_name = "User Type")
    is_active = models.BooleanField(default = True, help_text = "Designates whether the user should be considered active or not.", verbose_name = "Active Status")
    last_login = models.DateTimeField(default = datetime.datetime.now, help_text = "Designates the last login date and time of the user.", verbose_name = "Last Signin")
    groups = models.ManyToManyField(Group, null = True, help_text = "Designates the foreign key of the Group model.", verbose_name = "Groups")
    user_permissions = models.ManyToManyField(Permission, null = True, help_text = "Designates the foreign key of the Permission model.", verbose_name = "User Permissions")

    objects = AccountManager()
    USERNAME_FIELD = "username"

    class Meta:
        db_table = "auth_account"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
    
    @property
    def is_staff(self):
        if self.usertype.is_staff == False and self.usertype.is_superuser == True:
            return True
        
        if self.usertype.is_staff == True:
            return True
    
    @property
    def is_superuser(self):
        if self.usertype.is_staff == True and self.usertype.is_superuser == False:
            return True
        
        if self.usertype.is_superuser == True:
            return True

    def __str__(self):
        return str(self.username)


class User(models.Model):
    account = models.OneToOneField(Account, on_delete = models.SET_NULL, null = True, help_text = "Designates the foreign key of the Account model.", verbose_name = "Account")
    first_name = models.CharField(max_length = 65, null = True, help_text = "Designates the first name of the user.", verbose_name = "First Name")
    last_name = models.CharField(max_length = 65, null = True, help_text = "Designates the last name of the user.", verbose_name = "Last Name")
    email = models.EmailField(max_length = 65, null = True, help_text = "Designates the email of the user.", verbose_name = "Email")
    phone_number = models.IntegerField(validators = [MinValueValidator(0)], null = True, blank = True, help_text = "Designates the phone number of the user.", verbose_name = "Phone Number")
    profile_photo = models.ImageField(default = "profiles/default.png", null = True, upload_to = "profiles", help_text = "Designates the profile photo of the user.", verbose_name = "Profile Photo")
    joined_date = models.DateTimeField(default = datetime.datetime.now(), help_text = "Designates the joined date and time of the user.", verbose_name = "Joined Date")
    
    class Meta:
        db_table = "localaccount_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def gallery_photo(self):
        if self.profile_photo != "":
            return mark_safe("<img src = '%s%s'/>" % (f"{settings.MEDIA_URL}", self.profile_photo))
    
    gallery_photo.short_description = "Gallery Photo"

    def __str__(self):
        return str(self.account)
    

class Site2(Site):
    Site._meta.get_field("domain").help_text = "Designates the domain name of the site."
    Site._meta.get_field("domain").verbose_name = "Domain Name"
    Site._meta.get_field("name").help_text = "Designates the display name of the site."
    Site._meta.get_field("name").verbose_name = "Display Name"
    Site._meta.verbose_name = "Site"
    Site._meta.verbose_name_plural = "Sites"

    class Meta:
        app_label = "sites"
        managed = False

    def __str__(self):
        if Site._meta.get_field("domain"):
            return str(Site._meta.get_field("domain"))

        elif Site._meta.get_field("name"):
             return str(Site._meta.get_field("name"))


class SocialAccount2(SocialAccount):
    SocialAccount._meta.get_field("user").help_text = "Designates the username of the social account."
    SocialAccount._meta.get_field("user").verbose_name = "Username"
    SocialAccount._meta.get_field("provider").help_text = "Designates the provider name of the social account."
    SocialAccount._meta.get_field("provider").verbose_name = "Provider Name"
    SocialAccount._meta.get_field("uid").help_text = "Designates the unique identifier for the social account."
    SocialAccount._meta.get_field("uid").verbose_name = "User Identifier"
    SocialAccount._meta.get_field("extra_data").help_text = "Designates the extra information for the social account."
    SocialAccount._meta.get_field("extra_data").verbose_name = "Extra Information"
    SocialAccount._meta.verbose_name = "Account"
    SocialAccount._meta.verbose_name_plural = "Accounts"
    
    class Meta:
        app_label = "socialaccount"
        managed = False
    
    def __str__(self):
        return str(SocialAccount._meta.get_field("user"))


class SocialToken2(SocialToken):
    SocialToken._meta.get_field("app").help_text = "Designates the social application name for the token."
    SocialToken._meta.get_field("app").verbose_name = "Social Application"
    SocialToken._meta.get_field("account").help_text = "Designates the social account for the token."
    SocialToken._meta.get_field("account").verbose_name = "Social Account"
    SocialToken._meta.get_field("token").help_text = "Designates the token for the social account."
    SocialToken._meta.get_field("token").verbose_name = "Token"
    SocialToken._meta.get_field("token_secret").help_text = "Designates the encrpyted token for the social account."
    SocialToken._meta.get_field("token_secret").verbose_name = "Secret Token"
    SocialToken._meta.get_field("expires_at").verbose_name = "Expiration Date"
    SocialToken._meta.get_field("expires_at").help_text = "Designates the expiration date of the token."
    SocialToken._meta.verbose_name = "Social Token"
    SocialToken._meta.verbose_name_plural = "Social Tokens"

    class Meta:
        app_label = "socialaccount"
        managed = False
    
    def __str__(self):
        return str(SocialToken._meta.get_field("token"))
    

class SocialApp2(SocialApp):
    SocialApp._meta.get_field("provider").help_text = "Designates the provider name of the social account."
    SocialApp._meta.get_field("provider").verbose_name = "Provider Name"
    SocialApp._meta.get_field("provider_id").help_text = "Designates the unique identifier of the social account provider."
    SocialApp._meta.get_field("provider_id").verbose_name = "Provider ID"
    SocialApp._meta.get_field("name").help_text = "Designates the name of the social application."
    SocialApp._meta.get_field("name").verbose_name = "Social Application"
    SocialApp._meta.get_field("client_id").help_text = "Designates the unique identifier for the social application client."
    SocialApp._meta.get_field("client_id").verbose_name = "Client Identifier"
    SocialApp._meta.get_field("secret").help_text = "Designates the encrpyted key for the social application."
    SocialApp._meta.get_field("secret").verbose_name = "Secret Key"
    SocialApp._meta.get_field("key").help_text = "Designates the key for the social application."
    SocialApp._meta.get_field("key").verbose_name = "Key"
    SocialApp._meta.get_field("settings").help_text = "Designates the settings for the social application."
    SocialApp._meta.get_field("settings").verbose_name = "Settings"
    SocialApp._meta.verbose_name = "Social Application"
    SocialApp._meta.verbose_name_plural = "Social Applications"

    class Meta:
        app_label = "socialaccount"
        managed = False
    
    def __str__(self):
        return str(SocialApp._meta.get_field("provider"))