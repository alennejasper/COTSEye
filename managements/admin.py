from django.contrib import admin
from managements.models import *

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Location, LocationAdmin)


class StatusTypeAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(StatusType, StatusTypeAdmin)


class StatusAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Status, StatusAdmin)