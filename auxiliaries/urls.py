from django.urls import path
from auxiliaries import views

# Create your URL configuration here.
urlpatterns = [
    path("announcement/", views.PublicAnnouncement, name = "Public Announcement"),
    path("announcement/read/<int:id>", views.PublicAnnouncementRead, name = "Public Announcement Read"),
    path("contributor/announcement/", views.ContributorAnnouncement, name = "Contributor Announcement"),
    path("contributor/announcement/read/<int:id>", views.ContributorAnnouncementRead, name = "Contributor Announcement Read"),
]