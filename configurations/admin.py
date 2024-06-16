from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from authentications.views import AdministratorControlLogin, AdministratorControlLogout, ControlHomeRedirect, ControlPasswordRedirect, ControlProfileRedirect


# Register your models here.
class AdministratorSite(admin.AdminSite):    
    site_title = "Home"

    index_title = "COTSEYE"
    
    index_template = "admin/control/index/index.html"

    def login(self, request, extra_context = None):
        return super().login(request, extra_context)
    
    def has_permission(self, request):
        return request.user.is_active and request.user.usertype_id == 1

    def index(self, request, extra_context = None):
        if not self.has_permission(request):
            return HttpResponseRedirect(reverse("admin:login"))
        
        return super().index(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()

        urlpatterns = [
            path("login/", AdministratorControlLogin, name = "Administrator Control Login"),
            
            path("logout/", AdministratorControlLogout, name = "Administrator Control Logout"),

            path("home/redirect/", ControlHomeRedirect, name = "Control Home Redirect"),

            path("password/redirect/", ControlPasswordRedirect, name = "Control Password Redirect"),

            path("profile/redirect/", ControlProfileRedirect, name = "Control Profile Redirect")
        ]

        return urlpatterns + urls

admin.site = AdministratorSite(name = "admins")