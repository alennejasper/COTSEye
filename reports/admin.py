from django.contrib import admin
from reports.models import *

# Register your models here.
class CoordinatesAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Coordinates, CoordinatesAdmin)


class PostStatusAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(PostStatus, PostStatusAdmin)


class PostObservationsAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(PostObservations, PostObservationsAdmin)


class PostAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2

admin.site.register(Post, PostAdmin)