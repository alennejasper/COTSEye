from django.urls import path
from auxiliaries import views

# Create your URL configuration here.
urlpatterns = [
    path("announcement/service/", views.PublicServiceAnnouncement, name = "Public Service Announcement"),
    
    path("announcement/service/read/<int:id>/", views.PublicServiceAnnouncementRead, name = "Public Service Announcement Read"),

    path("contributor/service/announcement/", views.ContributorServiceAnnouncement, name = "Contributor Service Announcement"),
    
    path("contributor/service/announcement/read/<int:id>/", views.ContributorServiceAnnouncementRead, name = "Contributor Service Announcement Read"),
]