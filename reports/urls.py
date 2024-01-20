from django.urls import path
from reports import views

# Create your URL configuration here.
urlpatterns = [
    path("contributor/create/", views.ContributorCreate, name = "Contributor Create"),
    
    path("contributor/post/", views.ContributorPost, name = "Contributor Post"),
   
    path("contributor/post/uncertain", views.ContributorUncertain, name = "Contributor Uncertain"),
    
    path("contributor/post/uncertain/read/<int:id>", views.ContributorUncertainRead, name = "Contributor Uncertain Read"),
    
    path("contributor/post/uncertain/update/<int:id>", views.ContributorUncertainUpdate, name = "Contributor Uncertain Update"),
    
    path("contributor/post/valid", views.ContributorValid, name = "Contributor Valid"),
    
    path("contributor/post/valid/read/<int:id>", views.ContributorValidRead, name = "Contributor Valid Read"),
    
    path("contributor/post/invalid", views.ContributorInvalid, name = "Contributor Invalid"),
    
    path("contributor/post/invalid/read/<int:id>", views.ContributorInvalidRead, name = "Contributor Invalid Read"),
    
    path("contributor/post/invalid/delete/<int:id>", views.ContributorInvalidDelete, name = "Contributor Invalid Delete"),
]