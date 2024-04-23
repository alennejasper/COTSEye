from django.urls import path
from reports import views

# Create your URL configuration here.
urlpatterns = [    
    path("public/service/post/valid/", views.PublicServicePostValid, name = "Public Service Post Valid"),

    path("public/service/post/valid/read/<int:id>/", views.PublicServicePostValidRead, name = "Public Service Post Valid Read"),

    path("contributor/service/report/", views.ContributorServiceReport, name = "Contributor Service Report"),

    path("contributor/service/report/capture/", views.ContributorServiceReportCapture, name = "Contributor Service Report Capture"),

    path("contributor/service/report/choose/", views.ContributorServiceReportChoose, name = "Contributor Service Report Choose"),

    path("contributor/service/report/fetch/", views.ContributorServiceReportFetch, name = "Contributor Service Report Fetch"),

    path("contributor/service/report/update/<int:id>", views.ContributorServiceReportUpdate, name = "Contributor Service Report Update"),

    path("contributor/service/report/capture/update/<int:id>/", views.ContributorServiceReportCaptureUpdate, name = "Contributor Service Report Capture Update"),

    path("contributor/service/report/choose/update/<int:id>/", views.ContributorServiceReportChooseUpdate, name = "Contributor Service Report Choose Update"),

    path("contributor/service/report/update/fetch/", views.ContributorServiceReportUpdateFetch, name = "Contributor Service Report Update Fetch"),

    path("contributor/service/post/", views.ContributorServicePost, name = "Contributor Service Post"),

    path("contributor/service/post/valid/", views.ContributorServicePostValid, name = "Contributor Service Post Valid"),
    
    path("contributor/service/post/valid/read/<int:id>/", views.ContributorServicePostValidRead, name = "Contributor Service Post Valid Read"),
    
    path("contributor/service/post/invalid/", views.ContributorServicePostInvalid, name = "Contributor Service Post Invalid"),
    
    path("contributor/service/post/invalid/read/<int:id>/", views.ContributorServicePostInvalidRead, name = "Contributor Service Post Invalid Read"),
    
    path("contributor/service/post/invalid/delete/<int:id>/", views.ContributorServicePostInvalidDelete, name = "Contributor Service Post Invalid Delete"),

    path("contributor/service/post/invalid/delete/fetch/", views.ContributorServicePostInvalidDeleteFetch, name = "Contributor Service Post Invalid Delete Fetch"),

    path("contributor/service/post/uncertain/", views.ContributorServicePostUncertain, name = "Contributor Service Post Uncertain"),
    
    path("contributor/service/post/uncertain/read/<int:id>/", views.ContributorServicePostUncertainRead, name = "Contributor Service Post Uncertain Read"),

    path("contributor/service/post/draft/", views.ContributorServicePostDraft, name = "Contributor Service Post Draft"),

    path("contributor/service/post/draft/send/<int:id>/", views.ContributorServicePostDraftSend, name = "Contributor Service Post Draft Send"),

    path("contributor/service/post/draft/send/fetch/", views.ContributorServicePostDraftSendFetch, name = "Contributor Service Post Draft Send Fetch"),

    path("contributor/service/post/draft/read/<int:id>/", views.ContributorServicePostDraftRead, name = "Contributor Service Post Draft Read"),

    path("service/post/valid/read/redirect/", views.PostValidReadRedirect, name = "Post Valid Read Redirect"),
]