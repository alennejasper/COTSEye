from configurations.admin import officer, admin
from reports.models import *

# Register your models here.
class PostPhotoAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    readonly_fields = ["gallery_photo"]
    
officer.register(PostPhoto, PostPhotoAdmin)


class PostGalleryInline(admin.TabularInline):
    model = PostGallery
    extra = 0
    

class CoordinatesAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Coordinates, CoordinatesAdmin)


class PostStatusAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(PostStatus, PostStatusAdmin)


class DepthAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Depth, DepthAdmin)


class WeatherAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Weather, WeatherAdmin)


class PostObservationAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(PostObservation, PostObservationAdmin)


class PostAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Post, PostAdmin)


class PostPhotoAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    readonly_fields = ["gallery_photo"]

admin.site.register(PostPhoto, PostPhotoAdmin)


class PostGalleryInline(admin.TabularInline):
    model = PostGallery
    extra = 0


class CoordinatesAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Coordinates, CoordinatesAdmin)


class PostStatusAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(PostStatus, PostStatusAdmin)


class DepthAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Depth, DepthAdmin)


class WeatherAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Weather, WeatherAdmin)


class PostObservationAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }
        
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
admin.site.register(PostObservation, PostObservationAdmin)


class PostAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

    inlines = [PostGalleryInline]

admin.site.register(Post, PostAdmin)