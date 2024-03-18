"""
URL configuration for configurations project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
    
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name = "home")

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name = "home")

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from authentications import views
from configurations.admin import officer, admin

urlpatterns = [
    path("admin/database/login/", views.AdministratorDatabaseLogin),
    
    path("admin/database/logout/", views.AdministratorDatabaseLogout),
    
    path("admin/database/", admin.site.urls),

    path("officer/database/login/", views.OfficerDatabaseLogin),
    
    path("officer/database/logout/", views.OfficerDatabaseLogout),

    path("officer/database/", officer.urls),
    
    path("", include("allauth.urls")),
    
    path("", include("authentications.urls")),
    
    path("", include("reports.urls")),

    path("", include("managements.urls")),
    
    path("", include("auxiliaries.urls")),

    path("cache.js", (TemplateView.as_view(template_name = "webwares/cache.js", content_type = "application/javascript")), name = "cache.js")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)