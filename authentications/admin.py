from configurations.admin import admin
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from authentications.models import *


# Register your models here.
class UserTypeAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1

admin.site.register(UserType, UserTypeAdmin)


class AccountAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1

admin.site.register(Account, AccountAdmin)


class UserAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1

admin.site.register(User, UserAdmin)


class SiteAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1
    
    list_display = ("domain",)

admin.site.register(Site, SiteAdmin)


class SocialAccountAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,):
        return request.user.usertype_id == 1
    
    list_display = ("user",)

admin.site.register(SocialAccount, SocialAccountAdmin)


class SocialTokenAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,):
        return request.user.usertype_id == 1

    list_display = ("token",)

admin.site.register(SocialToken, SocialTokenAdmin)


class SocialAppAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,):
        return request.user.usertype_id == 1
    
    list_display = ("provider",)

admin.site.register(SocialApp, SocialAppAdmin)