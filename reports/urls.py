from django.urls import path
from reports import views

# Create your URL configuration here.
urlpatterns = [    
    path("contributor/post/", views.ContributorPost, name = "Contributor Post"),

    path("contributor/post/valid", views.ContributorPostValid, name = "Contributor Post Valid"),
    
    path("contributor/post/valid/read/<int:id>", views.ContributorPostValidRead, name = "Contributor Post Valid Read"),
    
    path("contributor/post/invalid", views.ContributorPostInvalid, name = "Contributor Post Invalid"),
    
    path("contributor/post/invalid/read/<int:id>", views.ContributorPostInvalidRead, name = "Contributor Post Invalid Read"),
    
    path("contributor/post/invalid/delete/<int:id>", views.ContributorPostInvalidDelete, name = "Contributor Post Invalid Delete"),

    path("contributor/post/uncertain", views.ContributorPostUncertain, name = "Contributor Post Uncertain"),
    
    path("contributor/post/uncertain/create/", views.ContributorPostUncertainCreate, name = "Contributor Post Uncertain Create"),

    path("contributor/post/uncertain/create/capture/", views.ContributorPostUncertainCreateCapture, name = "Contributor Post Uncertain Create Capture"),

    path("contributor/post/uncertain/create/choose/", views.ContributorPostUncertainCreateChoose, name = "Contributor Post Uncertain Create Choose"),

    path("contributor/post/uncertain/read/<int:id>", views.ContributorPostUncertainRead, name = "Contributor Post Uncertain Read"),

    path("contributor/post/uncertain/update/", views.ContributorPostUncertainUpdate, name = "Contributor Post Uncertain Update"),
        
    path("contributor/post/uncertain/update/capture/<int:id>", views.ContributorPostUncertainUpdate, name = "Contributor Post Uncertain Update Capture"),

    path("contributor/post/uncertain/update/choose/<int:id>", views.ContributorPostUncertainUpdate, name = "Contributor Post Uncertain Update Choose"),
]