from configurations.admin import admin, administrator
from managements.models import *


# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def get_form(self, request, obj = None, **kwargs):
        form = super(LocationAdmin, self).get_form(request, obj, **kwargs)

        municipality = form.base_fields["municipality"]

        municipality.widget.can_view_related = False

        municipality.widget.can_add_related = False

        municipality.widget.can_change_related = False

        municipality.widget.can_delete_related = False

        barangay = form.base_fields["barangay"]

        barangay.widget.can_view_related = False

        barangay.widget.can_add_related = False

        barangay.widget.can_change_related = False

        barangay.widget.can_delete_related = False

        return form
    
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)
    
    list_display = ["municipality", "barangay"]

    list_filter = ["municipality"]

    search_fields = ["municipality__municipality_name", "barangay__barangay_name"]

administrator.register(Location, LocationAdmin)

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
    
    list_display = ["statustype", "description"]

    search_fields = ["statustype"]

administrator.register(StatusType, StatusTypeAdmin)


class MunicipalityAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)
    
    list_display = ["municipality_name"]

    search_fields = ["municipality_name"]
    
administrator.register(Municipality, MunicipalityAdmin)


class BarangayAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
    
    def get_form(self, request, obj = None, **kwargs):
        form = super(BarangayAdmin, self).get_form(request, obj, **kwargs)

        municipality = form.base_fields["municipality"]

        municipality.widget.can_view_related = False

        municipality.widget.can_add_related = False

        municipality.widget.can_change_related = False

        municipality.widget.can_delete_related = False

        return form

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

    list_display = ["municipality", "barangay_name"]

    list_filter = ["municipality"]

    search_fields = ["barangay_name"]
    
administrator.register(Barangay, BarangayAdmin)


# class AnnouncementAdmin(admin.ModelAdmin):
#     class Media:   
#         css = {
#             "all": ["css/admin/control/index/index.css"]
#         }
        
#     def has_module_permission(self, request):
#         return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
#     def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
#        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

#        return super().render_change_form(request, context, add, change, form_url, obj)

#     readonly_fields = ["gallery_photo"]

# admin.site.register(Announcement, AnnouncementAdmin)


# class InterventionAdmin(admin.ModelAdmin):
#     class Media:   
#         css = {
#             "all": ["css/admin/control/index/index.css"]
#         }
        
#     def has_module_permission(self, request):
#         return request.user.usertype_id == 1 or request.user.usertype_id == 2

#     def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
#         context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

#     return super().render_change_form(request, context, add, change, form_url, obj)

#     readonly_fields = ["gallery_photo"]

# admin.site.register(Intervention, InterventionAdmin)


# class StatusAdmin(admin.ModelAdmin):
#     class Media:   
#         css = {
#             "all": ["css/admin/control/index/index.css"]
#         }

#     def has_module_permission(self, request):
#         return request.user.usertype_id == 1 or request.user.usertype_id == 2

#     def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
#         context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

#     return super().render_change_form(request, context, add, change, form_url, obj)

# admin.site.register(Status, StatusAdmin)