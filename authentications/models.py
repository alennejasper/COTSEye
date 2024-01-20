from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.contrib.sites.models import Site
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

        return self.create_user(username, password, **other_fields)


class UserType(models.Model):
    is_superuser = models.BooleanField(default = False, help_text = "Designates that the user can log into the administrator site.", verbose_name = "Administrator Status")
    is_staff = models.BooleanField(default = False, help_text = "Designates whether the user can log into the officers site.", verbose_name = "Officer Status")
    is_contributor = models.BooleanField(default = False, help_text = "Designates whether the user can log into the contributors site.", verbose_name = "Contributor Status")

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
    usertype = models.ForeignKey(UserType, on_delete = models.SET_NULL, blank = True, null = True, help_text = "Designates the foreign field of the User Type model.", verbose_name = "User Type")
    is_active = models.BooleanField(default = True, help_text = "Designates whether the user should be considered active or not.", verbose_name = "Active Status")
    last_login = models.DateTimeField(default = datetime.datetime.now, verbose_name = "Last Signin")
    groups = models.ManyToManyField(Group, blank = True, verbose_name = "Groups")
    user_permissions = models.ManyToManyField(Permission, blank = True, verbose_name = "User Permissions")

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
    account = models.OneToOneField(Account, on_delete = models.CASCADE, null = True, blank = True, help_text = "Designates the foreign field of the Account model.", verbose_name = "Account")
    first_name = models.CharField(max_length = 65, null = True, blank = True, help_text = "Designates the first name of the user.", verbose_name = "First Name")
    last_name = models.CharField(max_length = 65, null = True, blank = True, help_text = "Designates the last name of the user.", verbose_name = "Last Name")
    email = models.EmailField(max_length = 65, null = True, help_text = "Designates the email of the user.", verbose_name = "Email")
    phone_number = models.CharField(max_length = 10, null = True, blank = True, help_text = "Designates the phone number of the user.", verbose_name = "Phone Number")
    profile_photo = models.ImageField(default = "profiles/default.png", null = True, blank = True, upload_to = "profiles", help_text = "Designates the profile photo of the user.", verbose_name = "Profile Photo")
    joined_date = models.DateTimeField(auto_now_add = True, help_text = "Designates the joined date and time of the user.", verbose_name = "Joined Date")
    
    joined_date.editable = True

    class Meta:
        db_table = "localaccount_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

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
    SocialToken._meta.verbose_name = "Social Token"
    SocialToken._meta.verbose_name_plural = "Social Tokens"

    class Meta:
        app_label = "socialaccount"
    
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
    
    def __str__(self):
        return str(SocialApp._meta.get_field("provider"))