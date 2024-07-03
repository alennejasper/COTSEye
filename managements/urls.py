from django.urls import path
from managements import views

# Create your URL configuration here.
urlpatterns = [
    path("public/service/announcement/", views.PublicServiceAnnouncement, name = "Public Service Announcement"),
    
    path("public/service/announcement/read/<int:id>/", views.PublicServiceAnnouncementRead, name = "Public Service Announcement Read"),

    path("public/service/intervention/", views.PublicServiceIntervention, name = "Public Service Intervention"),

    path("public/service/intervention/read/<int:id>/", views.PublicServiceInterventionRead, name = "Public Service Intervention Read"),

    path("contributor/service/announcement/", views.ContributorServiceAnnouncement, name = "Contributor Service Announcement"),
    
    path("contributor/service/announcement/read/<int:id>/", views.ContributorServiceAnnouncementRead, name = "Contributor Service Announcement Read"),

    path("contributor/service/intervention/", views.ContributorServiceIntervention, name = "Contributor Service Intervention"),

    path("contributor/service/intervention/read/<int:id>/", views.ContributorServiceInterventionRead, name = "Contributor Service Intervention Read"),

    path("officer/control/announcement/", views.OfficerControlAnnouncement, name = "Officer Control Announcement"),

    path("officer/control/announcement/read/<int:id>/", views.OfficerControlAnnouncementRead, name = "Officer Control Announcement Read"),

    path("officer/control/announcement/add/", views.OfficerControlAnnouncementAdd, name = "Officer Control Announcement Add"),

    path("officer/control/announcement/update/<int:id>/", views.OfficerControlAnnouncementUpdate, name = "Officer Control Announcement Update"),

    path("officer/control/announcement/delete/<int:id>/", views.OfficerControlAnnouncementDelete, name = "Officer Control Announcement Delete"),

    path("officer/control/intervention/", views.OfficerControlIntervention, name = "Officer Control Intervention"),

    path("officer/control/intervention/read/<int:id>/", views.OfficerControlInterventionRead, name = "Officer Control Intervention Read"),

    path("officer/control/intervention/add/", views.OfficerControlInterventionAdd, name = "Officer Control Intervention Add"),

    path("officer/control/intervention/update/<int:id>/", views.OfficerControlInterventionUpdate, name = "Officer Control Intervention Update"),

    path("officer/control/intervention/delete/<int:id>/", views.OfficerControlInterventionDelete, name = "Officer Control Intervention Delete"),

    path("officer/control/status/", views.OfficerControlStatus, name = "Officer Control Status"),

    path("officer/control/status/municipality/read/<str:municipality_name>/", views.OfficerControlStatusMunicipalityRead, name = "Officer Control Status Municipality Read"),

    path("officer/control/status/barangay/read/<str:barangay_name>/", views.OfficerControlStatusBarangayRead, name = "Officer Control Status Barangay Read"),

    path("officer/control/status/add/", views.OfficerControlStatusAdd, name = "Officer Control Status Add"),

    path("officer/control/status/delete/<int:id>/", views.OfficerControlDeleteStatus, name = "Officer Control Status Delete"),

    path("officer/control/barangay/read/", views.OfficerControlBarangayRead, name = "Officer Control Barangay Read"),

    path("officer/control/report/", views.OfficerControlReport, name = "Officer Control Report"),
]