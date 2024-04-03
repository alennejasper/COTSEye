from django.urls import path
from auxiliaries import views

# Create your URL configuration here.
urlpatterns = [
    path("public/service/announcement/", views.PublicServiceAnnouncement, name = "Public Service Announcement"),
    
    path("public/service/announcement/read/<int:id>/", views.PublicServiceAnnouncementRead, name = "Public Service Announcement Read"),

    path("public/service/resource/", views.PublicServiceResource, name = "Public Service Resource"),

    path("public/service/resource/link/", views.PublicServiceResourceLink, name = "Public Service Resource Link"),

    path("public/service/resource/file/", views.PublicServiceResourceFile, name = "Public Service Resource File"),

    path("public/service/inquiry/", views.PublicServiceInquiry, name = "Public Service Inquiry"),

    path("contributor/service/announcement/", views.ContributorServiceAnnouncement, name = "Contributor Service Announcement"),
    
    path("contributor/service/announcement/read/<int:id>/", views.ContributorServiceAnnouncementRead, name = "Contributor Service Announcement Read"),

    path("contributor/service/resource/", views.ContributorServiceResource, name = "Contributor Service Resource"),

    path("contributor/service/resource/link/", views.ContributorServiceResourceLink, name = "Contributor Service Resource Link"),

    path("contributor/service/resource/file/", views.ContributorServiceResourceFile, name = "Contributor Service Resource File"),

    path("service/resource/link/read/<int:id>/redirect/", views.ServiceResourceLinkReadRedirect, name = "Service Resource Link Read Redirect"),

    path("service/resource/file/read/<int:id>/redirect/", views.ServiceResourceFileReadRedirect, name = "Service Resource File Read Redirect")
]