from configurations.admin import admin, administrator
from auxiliaries.models import *

# Register your models here.
class LinkAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

    list_display = ["title", "author"]

    search_fields = ["title"]

administrator.register(Link, LinkAdmin)


class FileAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)
    
    list_display = ["title", "author"]

    search_fields = ["title"]

administrator.register(File, FileAdmin)


class InquiryAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)
    
    search_fields = ["question"]

administrator.register(Inquiry, InquiryAdmin)