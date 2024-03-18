from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse


# Register your models here.
class AdministratorSite(admin.AdminSite):    
    admin.site.site_title = "Home"

    index_title = "COTSEye"
    
    index_template = "admin/database/index/index.html"

    def login(self, request, extra_context = None):
        return super().login(request, extra_context)
    
    def has_permission(self, request):
        return request.user.is_active and request.user.usertype_id == 1

    def index(self, request, extra_context = None):
        if not self.has_permission(request):
            return HttpResponseRedirect(reverse("admin:login"))
        
        return super().index(request, extra_context)

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

officer = OfficerSite(name = "officer")