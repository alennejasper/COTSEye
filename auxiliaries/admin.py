from configurations.admin import officer, admin
from auxiliaries.models import *

# Register your models here.
class AnnouncementAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/database/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Announcement, AnnouncementAdmin)


class AnnouncementAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/database/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Announcement, AnnouncementAdmin)