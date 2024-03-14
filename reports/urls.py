from django.urls import path
from reports import views

# Create your URL configuration here.
urlpatterns = [    
    path("contributor/service/post/", views.ContributorServicePost, name = "Contributor Service Post"),

    path("contributor/service/post/valid/", views.ContributorServicePostValid, name = "Contributor Service Post Valid"),
    
    path("contributor/service/post/valid/read/<int:id>/", views.ContributorServicePostValidRead, name = "Contributor Service Post Valid Read"),
    
    path("contributor/service/post/valid/reads/<int:id>/", views.ContributorServicePostValidReads, name = "Contributor Service Post Valid Reads"),

    path("contributor/service/post/invalid/", views.ContributorServicePostInvalid, name = "Contributor Service Post Invalid"),
    
    path("contributor/service/post/invalid/read/<int:id>/", views.ContributorServicePostInvalidRead, name = "Contributor Service Post Invalid Read"),
    
    path("contributor/service/post/invalid/delete/<int:id>/", views.ContributorServicePostInvalidDelete, name = "Contributor Service Post Invalid Delete"),

    path("contributor/service/post/uncertain/", views.ContributorServicePostUncertain, name = "Contributor Service Post Uncertain"),
    
    path("contributor/service/post/uncertain/create/", views.ContributorServicePostUncertainCreate, name = "Contributor Service Post Uncertain Create"),

    path("contributor/service/post/uncertain/create/capture/", views.ContributorServicePostUncertainCreateCapture, name = "Contributor Service Post Uncertain Create Capture"),

    path("contributor/service/post/uncertain/create/choose/", views.ContributorServicePostUncertainCreateChoose, name = "Contributor Service Post Uncertain Create Choose"),

    path("contributor/service/post/uncertain/read/<int:id>/", views.ContributorServicePostUncertainRead, name = "Contributor Service Post Uncertain Read"),

    path("contributor/service/post/uncertain/read/<int:id>/update/", views.ContributorServicePostUncertainUpdate, name = "Contributor Service Post Uncertain Update"),
        
    path("contributor/service/post/uncertain/read/<int:id>/update/capture/", views.ContributorServicePostUncertainUpdateCapture, name = "Contributor Service Post Uncertain Update Capture"),

    path("contributor/service/post/uncertain/read/<int:id>/update/choose/", views.ContributorServicePostUncertainUpdateChoose, name = "Contributor Service Post Uncertain Update Choose"),
]