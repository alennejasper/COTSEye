from configurations.admin import admin
from auxiliaries.models import *

# Register your models here.
class AnnouncementAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    readonly_fields = ["gallery_photo"]

admin.site.register(Announcement, AnnouncementAdmin)



class LinkAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Link, LinkAdmin)


class FileAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(File, FileAdmin)


class InquiryAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Inquiry, InquiryAdmin)