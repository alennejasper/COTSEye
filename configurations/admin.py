from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from authentications.views import OfficerControlRegister, OfficerControlLogin, OfficerControlLoginGoogle, OfficerControlLoginFacebook, OfficerControlStatistics, OfficerControlLogout, AdministratorControlLogin, AdministratorControlStatistics, AdministratorControlLogout, ControlHomeRedirect, ControlPasswordRedirect, ControlProfileRedirect
from managements.views import OfficerControlStatisticsStatus, OfficerControlStatisticsIntervention, AdministratorControlStatisticsStatus, AdministratorControlStatisticsIntervention, ControlStatisticsStatusReadRedirect, ControlStatisticsInterventionReadRedirect
from reports.views import OfficerControlStatisticsPost, AdministratorControlStatisticsPost, ControlStatisticsPostReadRedirect


# Register your models here.
class AdministratorSite(admin.AdminSite):    
    admin.site.site_title = "Home"

    index_title = "COTSEye"
    
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

            path("statistics/", AdministratorControlStatistics, name = "Administrator Control Statistics"),

            path("statistics/post/", AdministratorControlStatisticsPost, name = "Administrator Control Statistics Post"),

            path("statistics/status/", AdministratorControlStatisticsStatus, name = "Administrator Control Statistics Status"),

            path("statistics/intervention/", AdministratorControlStatisticsIntervention, name = "Administrator Control Statistics Intervention"),
            
            path("logout/", AdministratorControlLogout, name = "Administrator Control Logout"),

            path("home/redirect/", ControlHomeRedirect, name = "Control Home Redirect"),

            path("password/redirect/", ControlPasswordRedirect, name = "Control Password Redirect"),

            path("profile/redirect/", ControlProfileRedirect, name = "Control Profile Redirect"),

            path("statistics/post/read/<int:object_id>/redirect/", ControlStatisticsPostReadRedirect, name = "Control Statistics Post Read Redirect"),

            path("statistics/status/read/<int:object_id>/redirect/", ControlStatisticsStatusReadRedirect, name = "Control Statistics Status Read Redirect"),

            path("statistics/intervention/read/<int:object_id>/redirect/", ControlStatisticsInterventionReadRedirect, name = "Control Statistics Intervention Read Redirect")
        ]

        return urlpatterns + urls

admin.site = AdministratorSite(name = "admin")

class OfficerSite(admin.AdminSite):
    admin.site.site_title = "Home"
    
    index_title = "COTSEye"
    
    index_template = "officer/database/index/index.html"

    def login(self, request, extra_context = None):
        return super().login(request, extra_context)
    
    def has_permission(self, request):
        return request.user.is_active and request.user.usertype_id == 2

    def index(self, request, extra_context = None):
        if not self.has_permission(request):
            return HttpResponseRedirect(reverse("officer:login"))
        
        return super().index(request, extra_context)
    
    def get_urls(self):
        urls = super().get_urls()

        urlpatterns = [
            path("register/", OfficerControlRegister, name = "Officer Control Register"),

            path("login/", OfficerControlLogin, name = "Officer Control Login"),

            path("login/facebook/", OfficerControlLoginFacebook, name = "Officer Control Login Facebook"),

            path("login/google/", OfficerControlLoginGoogle, name = "Officer Control Login Google"),

            path("statistics/home/", OfficerControlStatistics, name = "Officer Control Statistics"),

            path("statistics/post/", OfficerControlStatisticsPost, name = "Officer Control Statistics Post"),

            path("statistics/status/", OfficerControlStatisticsStatus, name = "Officer Control Statistics Status"),

            path("statistics/intervention/", OfficerControlStatisticsIntervention, name = "Officer Control Statistics Intervention"),

            path("logout/", OfficerControlLogout, name = "Officer Control Logout"),         

            path("home/redirect/", ControlHomeRedirect, name = "Control Home Redirect"),

            path("password/redirect/", ControlPasswordRedirect, name = "Control Password Redirect"),

            path("profile/redirect/", ControlProfileRedirect, name = "Control Profile Redirect"),

            path("statistics/post/read/<int:object_id>/redirect/", ControlStatisticsPostReadRedirect, name = "Control Statistics Post Read Redirect"),

            path("statistics/status/read/<int:object_id>/redirect/", ControlStatisticsStatusReadRedirect, name = "Control Statistics Status Read Redirect"),

            path("statistics/intervention/read/<int:object_id>/redirect/", ControlStatisticsInterventionReadRedirect, name = "Control Statistics Intervention Read Redirect")
        ]

        return urlpatterns + urls
    
officer = OfficerSite(name = "officer")