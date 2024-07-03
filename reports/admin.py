from configurations.admin import admin, administrator
from reports.models import *


# Register your models here.
# class PostPhotoAdmin(admin.ModelAdmin):
#     class Media:   
#         css = {
#             "all": ["css/admin/control/index/index.css"]
#         }

#     def has_module_permission(self, request):
#         return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
#     readonly_fields = ["gallery_photo"]

#     def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
#         context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

#     return super().render_change_form(request, context, add, change, form_url, obj)

# admin.site.register(PostPhoto, PostPhotoAdmin)


# class PostGalleryInline(admin.TabularInline):
#     model = PostGallery
#     extra = 0


# class CoordinatesAdmin(admin.ModelAdmin):
#     class Media:   
#         css = {
#             "all": ["css/admin/control/index/index.css", "css/admin/control/form/coordinates.css"]
#         }

#     def has_module_permission(self, request):
#         return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
#     change_form_template = "admin/control/form/coordinates.html"

#     def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
#         context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

#     return super().render_change_form(request, context, add, change, form_url, obj)

# admin.site.register(Coordinates, CoordinatesAdmin)


# class PostStatusAdmin(admin.ModelAdmin):
#     class Media:   
#         css = {
#             "all": ["css/admin/control/index/index.css"]
#         }

#     def has_module_permission(self, request):
#         return request.user.usertype_id == 1 or request.user.usertype_id == 2

#     def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
#         context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

#     return super().render_change_form(request, context, add, change, form_url, obj)

# admin.site.register(PostStatus, PostStatusAdmin)


class SizeAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

    list_display = ["size"]

    search_fields = ["size"]

administrator.register(Size, SizeAdmin)


class DepthAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

    list_display = ["depth"]

    search_fields = ["depth"]

administrator.register(Depth, DepthAdmin)


class WeatherAdmin(admin.ModelAdmin):
    class Media:   
        css = {
            "all": ["css/admin/control/index/index.css"]
        }

    def has_module_permission(self, request):
        return request.user.usertype_id == 1 or request.user.usertype_id == 2
    
    def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
        context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

        return super().render_change_form(request, context, add, change, form_url, obj)

    list_display = ["weather"]

    search_fields = ["weather"]

administrator.register(Weather, WeatherAdmin)


# class PostObservationAdmin(admin.ModelAdmin):
#     class Media:   
#         css = {
#             "all": ["css/admin/control/index/index.css"]
#         }
        
#     def has_module_permission(self, request):
#         return request.user.usertype_id == 1 or request.user.usertype_id == 2

#     def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
#         context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

#     return super().render_change_form(request, context, add, change, form_url, obj)

# admin.site.register(PostObservation, PostObservationAdmin)


# class PostAdmin(admin.ModelAdmin):
#     class Media:   
#         css = {
#             "all": ["css/admin/control/index/index.css", "css/admin/control/form/post.css"]
#         }

#     def change_view(self, request, object_id, form_url = "", extra_context = None):
#         object = self.get_object(request, object_id)
        
#         if object is not None:
#             extra_context = extra_context or {}

#             extra_context["edition"] = True

#         return super().change_view(request, object_id, form_url, extra_context)
    
#     def has_module_permission(self, request):
#         return request.user.usertype_id == 1 or request.user.usertype_id == 2

#     inlines = [PostGalleryInline]

#     change_form_template = "admin/control/form/post.html"

#     def render_change_form(self, request, context, add = False, change = False, form_url = "", obj = None):
#         context.update({"show_save": True, "show_save_and_continue": False, "show_save_and_add_another": False, "show_delete": True})

#     return super().render_change_form(request, context, add, change, form_url, obj)

# admin.site.register(Post, PostAdmin)