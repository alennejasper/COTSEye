from django.urls import path
from reports import views

# Create your URL configuration here.
urlpatterns = [    
    path("contributor/service/report/", views.ContributorServiceReport, name = "Contributor Service Report"),

    path("contributor/service/report/capture/", views.ContributorServiceReportCapture, name = "Contributor Service Report Capture"),

    path("contributor/service/report/choose/", views.ContributorServiceReportChoose, name = "Contributor Service Report Choose"),

    path("contributor/service/report/update/capture/<int:id>/", views.ContributorServiceReportCaptureUpdate, name = "Contributor Service Report Capture Update"),

    path("contributor/service/report/update/choose/<int:id>/", views.ContributorServiceReportChooseUpdate, name = "Contributor Service Report Choose Update"),

    path("contributor/service/post/", views.ContributorServicePost, name = "Contributor Service Post"),

    path("contributor/service/post/valid/", views.ContributorServicePostValid, name = "Contributor Service Post Valid"),
    
    path("contributor/service/post/valid/read/<int:id>/", views.ContributorServicePostValidRead, name = "Contributor Service Post Valid Read"),
    
    path("contributor/service/post/invalid/", views.ContributorServicePostInvalid, name = "Contributor Service Post Invalid"),
    
    path("contributor/service/post/invalid/read/<int:id>/", views.ContributorServicePostInvalidRead, name = "Contributor Service Post Invalid Read"),
    
    path("contributor/service/post/invalid/delete/<int:id>/", views.ContributorServicePostInvalidDelete, name = "Contributor Service Post Invalid Delete"),

    path("contributor/service/post/uncertain/", views.ContributorServicePostUncertain, name = "Contributor Service Post Uncertain"),
    
    path("contributor/service/post/uncertain/read/<int:id>/", views.ContributorServicePostUncertainRead, name = "Contributor Service Post Uncertain Read"),

    path("service/post/valid/read/redirect/", views.ServicePostValidReadRedirect, name = "Service Post Valid Read Redirect"),
]