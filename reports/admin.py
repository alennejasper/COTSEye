from configurations.admin import officer, admin
from reports.models import *

# Register your models here.
class PostPhotosAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(PostPhotos, PostPhotosAdmin)


class CoordinatesAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Coordinates, CoordinatesAdmin)


class PostStatusAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(PostStatus, PostStatusAdmin)


class DepthAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Depth, DepthAdmin)


class WeatherAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Weather, WeatherAdmin)


class PostObservationAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(PostObservation, PostObservationAdmin)


class PostAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

officer.register(Post, PostAdmin)


class PostPhotosAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(PostPhotos, PostPhotosAdmin)


class CoordinatesAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Coordinates, CoordinatesAdmin)


class PostStatusAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(PostStatus, PostStatusAdmin)


class DepthAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Depth, DepthAdmin)


class WeatherAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Weather, WeatherAdmin)


class PostObservationAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(PostObservation, PostObservationAdmin)


class PostAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Post, PostAdmin)