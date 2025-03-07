from django.urls import path
from managements import views

# Create your URL configuration here.
urlpatterns = [
    path("public/service/announcement/", views.PublicServiceAnnouncement, name = "Public Service Announcement"),
    
    path("public/service/announcement/read/<int:id>/", views.PublicServiceAnnouncementRead, name = "Public Service Announcement Read"),

    path("public/service/activity/", views.PublicServiceActivity, name = "Public Service Activity"),

    path("public/service/activity/read/<int:id>/", views.PublicServiceActivityRead, name = "Public Service Activity Read"),

    path("contributor/service/announcement/", views.ContributorServiceAnnouncement, name = "Contributor Service Announcement"),
    
    path("contributor/service/announcement/read/<int:id>/", views.ContributorServiceAnnouncementRead, name = "Contributor Service Announcement Read"),

    path("contributor/service/activity/", views.ContributorServiceActivity, name = "Contributor Service Activity"),

    path("contributor/service/activity/read/<int:id>/", views.ContributorServiceActivityRead, name = "Contributor Service Activity Read"),

    path("curator/control/announcement/", views.CuratorControlAnnouncement, name = "Curator Control Announcement"),

    path("curator/control/announcement/read/<int:id>/", views.CuratorControlAnnouncementRead, name = "Curator Control Announcement Read"),

    path("curator/control/announcement/add/", views.CuratorControlAnnouncementAdd, name = "Curator Control Announcement Add"),

    path("curator/control/announcement/update/<int:id>/", views.CuratorControlAnnouncementUpdate, name = "Curator Control Announcement Update"),

    path("curator/control/announcement/delete/<int:id>/", views.CuratorControlAnnouncementDelete, name = "Curator Control Announcement Delete"),

    path("curator/control/activity/", views.CuratorControlActivity, name = "Curator Control Activity"),

    path("curator/control/activity/read/<int:id>/", views.CuratorControlActivityRead, name = "Curator Control Activity Read"),

    path("curator/control/activity/add/", views.CuratorControlActivityAdd, name = "Curator Control Activity Add"),

    path("curator/control/activity/update/<int:id>/", views.CuratorControlActivityUpdate, name = "Curator Control Activity Update"),

    path("curator/control/activity/delete/<int:id>/", views.CuratorControlActivityDelete, name = "Curator Control Activity Delete"),

    path("curator/control/status/", views.CuratorControlStatus, name = "Curator Control Status"),

    path("curator/control/status/municipality/read/<str:municipality_name>/", views.CuratorControlStatusMunicipalityRead, name = "Curator Control Status Municipality Read"),

    path("curator/control/status/barangay/read/<str:barangay_name>/", views.CuratorControlStatusBarangayRead, name = "Curator Control Status Barangay Read"),

    path("curator/control/status/add/", views.CuratorControlStatusAdd, name = "Curator Control Status Add"),

    path("curator/control/status/delete/<int:id>/", views.CuratorControlDeleteStatus, name = "Curator Control Status Delete"),

    path("curator/control/barangay/read/", views.CuratorControlBarangayRead, name = "Curator Control Barangay Read"),

    path("curator/control/report/", views.CuratorControlReport, name = "Curator Control Report"),
]