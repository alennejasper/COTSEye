from configurations.admin import officer, admin
from auxiliaries.models import *

# Register your models here.
class AnnouncementAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    readonly_fields = ["gallery_photo"]

officer.register(Announcement, AnnouncementAdmin)


class ResourceAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Resource, ResourceAdmin)


class ResourceFileAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(ResourceFile, ResourceFileAdmin)


class ResourceFileAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(ResourceFile, ResourceFileAdmin)


class ResourceLinkAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(ResourceLink, ResourceLinkAdmin)


class AnnouncementAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    readonly_fields = ["gallery_photo"]

admin.site.register(Announcement, AnnouncementAdmin)


class ResourceAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Resource, ResourceAdmin)


class ResourceLinkAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(ResourceLink, ResourceLinkAdmin)


class InquiryAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Inquiry, InquiryAdmin)


class InquiryAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Inquiry, InquiryAdmin)