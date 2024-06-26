from django.urls import path
from auxiliaries import views

# Create your URL configuration here.
urlpatterns = [
    path("public/service/announcement/", views.PublicServiceAnnouncement, name = "Public Service Announcement"),
    
    path("public/service/announcement/read/<int:id>/", views.PublicServiceAnnouncementRead, name = "Public Service Announcement Read"),

    path("public/service/resource/", views.PublicServiceResource, name = "Public Service Resource"),

    path("public/service/inquiry/", views.PublicServiceInquiry, name = "Public Service Inquiry"),

    path("public/service/map/", views.PublicServiceMap, name = "Public Service Map"),

    path("contributor/service/announcement/", views.ContributorServiceAnnouncement, name = "Contributor Service Announcement"),
    
    path("contributor/service/announcement/read/<int:id>/", views.ContributorServiceAnnouncementRead, name = "Contributor Service Announcement Read"),

    path("contributor/service/resource/", views.ContributorServiceResource, name = "Contributor Service Resource"),

    path("contributor/service/inquiry/", views.ContributorServiceInquiry, name = "Contributor Service Inquiry"),

    path("contributor/service/map/", views.ContributorServiceMap, name = "Contributor Service Map"),

    path("officer/control/announcement", views.OfficerControlAnnouncement, name = "Officer Control Announcement"),

    path("officer/control/announcement/add", views.officercontroladdannouncement, name = "Officer Control Add Announcement"),

    path("officer/control/announcement/update/<int:pk>", views.officercontrolupdateannouncement, name = "Officer Control Update Announcement"),

    path("officer/control/announcement/delete/<int:pk>/", views.officercontroldeleteannouncement, name = "Officer Control Delete Announcement"),

    path("officer/control/announcement/<int:pk>/", views.officer_control_announcement, name = "Officer Control Announcement"),

    path("service/link/read/<int:id>/redirect/", views.ServiceLinkReadRedirect, name = "Service Link Read Redirect"),

    path("service/file/read/<int:id>/redirect/", views.ServiceFileReadRedirect, name = "Service File Read Redirect"),
    
    path("get_barangays/", views.get_barangays, name = "get_barangays")
]