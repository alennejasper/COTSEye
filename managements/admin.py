from configurations.admin import officer, admin
from managements.models import *


# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Location, LocationAdmin)


class StatusTypeAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(StatusType, StatusTypeAdmin)


class StatusAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Status, StatusAdmin)


class InterventionAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Intervention, InterventionAdmin)

class LocationAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Location, LocationAdmin)

class StatusTypeAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(StatusType, StatusTypeAdmin)


class StatusAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Status, StatusAdmin)


class InterventionAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Intervention, InterventionAdmin)