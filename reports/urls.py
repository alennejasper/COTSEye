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

    path("contributor/service/post/draft/delete/<int:id>", views.ContributorServicePostDraftDelete, name = "Contributor Service Post Draft Delete"),

    path("contributor/service/post/draft/delete/fetch/", views.ContributorServicePostDraftDeleteFetch, name = "Contributor Service Post Draft Delete Fetch"),

    path("contributor/service/post/draft/update/<int:id>", views.ContributorServicePostDraftUpdate, name = "Contributor Service Post Draft Update"),

    path("contributor/service/post/draft/update/fetch/", views.ContributorServicePostDraftUpdateFetch, name = "Contributor Service Post Draft Update Fetch"),
    
    path("contributor/service/post/draft/send/<int:id>/", views.ContributorServicePostDraftSend, name = "Contributor Service Post Draft Send"),

    path("contributor/service/post/draft/send/fetch/", views.ContributorServicePostDraftSendFetch, name = "Contributor Service Post Draft Send Fetch"),

    path("officer/control/sighting/", views.OfficerControlSighting, name = "Officer Control Sighting"),
    
    path('officer/control/sighting/update/<int:id>/', views.OfficerControlSightingUpdate, name='officer_control_sighting_update'),

    path("officer/control/sighting/read/<int:id>/", views.OfficerControlSightingRead, name = "Officer Control Sighting Read"),

    path("officer/control/sighting/read/<int:object_id>/redirect/", views.OfficerControlSightingReadRedirect, name = "Officer Control Sighting Read Redirect"),

    path("sightings/control/sighting/valid/", views.OfficerControlSightingValid, name = "Officer Control Sighting Valid"),

    path("sightings/control/sighting/invalid", views.OfficerControlSightingInvalid, name = "Officer Control Sighting Invalid"),
    
    path("service/post/valid/read/<int:id>/redirect/", views.PostValidReadRedirect, name = "Post Valid Read Redirect"),

    path("mark_post_as_read/<int:id>/", views.mark_post_as_read, name = "mark_post_as_read"),

    path("api/posts/update/<int:post_id>/", views.update_post, name = "update_post"),   
    
    path("officer/control/sighting/delete_photo/<int:photo_id>/", views.DeletePostPhoto, name = "delete_photo"),

    path("post/<int:post_id>/add-remark/", views.add_remark, name = "add_remark")
]