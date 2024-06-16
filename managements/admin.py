from configurations.admin import admin
from managements.models import *


# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

admin.site.register(Location, LocationAdmin)

class StatusTypeAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

admin.site.register(StatusType, StatusTypeAdmin)


""" class StatusAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Status, StatusAdmin) """


""" class InterventionAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

    readonly_fields = ["gallery_photo"]

admin.site.register(Intervention, InterventionAdmin) """