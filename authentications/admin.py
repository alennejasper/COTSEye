from configurations.admin import admin, administrator
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from authentications.models import *


# Register your models here.
class UserTypeAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1

administrator.register(UserType, UserTypeAdmin)


class AccountAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_add_permission(self, request, obj = None):
        return False

    def has_module_permission(self, request):
        return request.user.usertype_id == 1
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)
    
    fields = ["username", "usertype", "is_active"]

    list_display = ["username", "last_login"]

    list_filter = ["usertype"]

    search_fields = ["username"]

administrator.register(Account, AccountAdmin)


# class UserAdmin(admin.ModelAdmin):
#     class Media:   
#         css = {
#             "all": ["css/admin/control/index/index.css"]
#         }

#     def has_module_permission(self, request):
#         return request.user.usertype_id == 1
    
#     def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
#         context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

#         return super().render_change_form(request, context, add, change, form_url, obj)

# admin.site.register(User, UserAdmin)


class SiteAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1
    
    list_display = ["domain",]

    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

administrator.register(Site, SiteAdmin)


class SocialAccountAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request,):
        return request.user.usertype_id == 1
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

    list_display = ("user",)
    
administrator.register(SocialAccount, SocialAccountAdmin)


class SocialTokenAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request,):
        return request.user.usertype_id == 1

    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

    list_display = ("token",)

administrator.register(SocialToken, SocialTokenAdmin)


class SocialAppAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request,):
        return request.user.usertype_id == 1
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

    list_display = ("provider",)

administrator.register(SocialApp, SocialAppAdmin)