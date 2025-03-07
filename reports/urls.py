from django.urls import path
from reports import views

# Create your URL configuration here.
urlpatterns = [    
    path("public/service/post/feed/", views.PublicServicePostFeed, name = "Public Service Post Feed"),

    path("public/service/post/feed/read/<int:id>/", views.PublicServicePostFeedRead, name = "Public Service Post Feed Read"),

    path("contributor/service/report/", views.ContributorServiceReport, name = "Contributor Service Report"),

    path("contributor/service/report/fetch/", views.ContributorServiceReportFetch, name = "Contributor Service Report Fetch"),

    path("contributor/service/post/", views.ContributorServicePost, name = "Contributor Service Post"),

    path("contributor/service/post/read/<int:id>/", views.ContributorServicePostRead, name = "Contributor Service Post Read"),

    path("contributor/service/post/feed/", views.ContributorServicePostFeed, name = "Contributor Service Post Feed"),

    path("contributor/service/post/feed/read/<int:id>/", views.ContributorServicePostFeedRead, name = "Contributor Service Post Feed Read"),
                
    path("contributor/service/post/invalid/delete/<int:id>/", views.ContributorServicePostInvalidDelete, name = "Contributor Service Post Invalid Delete"),

    path("contributor/service/post/invalid/delete/fetch/", views.ContributorServicePostInvalidDeleteFetch, name = "Contributor Service Post Invalid Delete Fetch"),

    path("contributor/service/post/draft/update/<int:id>", views.ContributorServicePostDraftUpdate, name = "Contributor Service Post Draft Update"),

    path("contributor/service/post/draft/update/fetch/", views.ContributorServicePostDraftUpdateFetch, name = "Contributor Service Post Draft Update Fetch"),

    path("contributor/service/post/draft/delete/<int:id>", views.ContributorServicePostDraftDelete, name = "Contributor Service Post Draft Delete"),

    path("contributor/service/post/draft/delete/fetch/", views.ContributorServicePostDraftDeleteFetch, name = "Contributor Service Post Draft Delete Fetch"),
    
    path("contributor/service/post/draft/send/<int:id>/", views.ContributorServicePostDraftSend, name = "Contributor Service Post Draft Send"),

    path("contributor/service/post/draft/send/fetch/", views.ContributorServicePostDraftSendFetch, name = "Contributor Service Post Draft Send Fetch"),

    path("curator/control/sighting/", views.CuratorControlSighting, name = "Curator Control Sighting"),
    
    path("curator/control/sighting/fetch/<int:id>/", views.CuratorControlSightingFetch, name = "Curator Control Sighting Fetch"),

    path("curator/control/sighting/read/<int:id>/", views.CuratorControlSightingRead, name = "Curator Control Sighting Read"),

    path("curator/control/sighting/read/<int:id>/redirect/", views.CuratorControlSightingReadRedirect, name = "Curator Control Sighting Read Redirect"),

    path("curator/control/sighting/add/<int:id>/", views.CuratorControlSightingAdd, name = "Curator Control Sighting Add"),

    path("curator/control/sighting/update/<int:id>/", views.CuratorControlSightingUpdate, name = "Curator Control Sighting Update"),

    path("curator/control/sighting/location/update/<int:id>/", views.CuratorControlSightingLocationUpdate, name = "Curator Control Sighting Location Update"), 

    path("curator/control/sighting/valid/", views.CuratorControlSightingValid, name = "Curator Control Sighting Valid"),

    path("curator/control/sighting/invalid/", views.CuratorControlSightingInvalid, name = "Curator Control Sighting Invalid"),
    
    path("curator/control/sighting/delete/<int:id>/", views.CuratorControlSightingDelete, name = "Curator Control Sighting Delete"),

    path("service/post/valid/read/<int:id>/redirect/", views.PostValidReadRedirect, name = "Post Valid Read Redirect"),
] 