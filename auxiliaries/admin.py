from django.contrib import admin
from auxiliaries.models import *

# Register your models here.
class AnnouncementAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Announcement, AnnouncementAdmin)