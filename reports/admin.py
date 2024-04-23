from configurations.admin import officer, admin
from reports.models import *

# Register your models here.
class PostPhotoAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/officer/control/index/index.css"]
        }

    def change_view(self, request, object_id, form_url = "", extra_context = None):
        object = self.get_object(request, object_id)
        
        if object is not None:
            extra_context = extra_context or {}

            extra_context["edition"] = True

        return super().change_view(request, object_id, form_url, extra_context)
    
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
            "all": ["css/officer/control/index/index.css", "css/officer/control/form/coordinates.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    change_form_template = "officer/control/form/coordinates.html"

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
            "all": ["css/officer/control/index/index.css", "css/admin/control/form/post.css"]
        }

    def change_view(self, request, object_id, form_url = "", extra_context = None):
        object = self.get_object(request, object_id)
        
        if object is not None:
            extra_context = extra_context or {}

            extra_context["edition"] = True

        return super().change_view(request, object_id, form_url, extra_context)
    
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

    inlines = [PostGalleryInline]

    change_form_template = "officer/control/form/post.html"

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
            "all": ["css/admin/control/index/index.css", "css/admin/control/form/coordinates.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    change_form_template = "admin/control/form/coordinates.html"

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
            "all": ["css/admin/control/index/index.css", "css/admin/control/form/post.css"]
        }

    def change_view(self, request, object_id, form_url = "", extra_context = None):
        object = self.get_object(request, object_id)
        
        if object is not None:
            extra_context = extra_context or {}

            extra_context["edition"] = True

        return super().change_view(request, object_id, form_url, extra_context)
    
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

    inlines = [PostGalleryInline]

    change_form_template = "admin/control/form/post.html"

admin.site.register(Post, PostAdmin)