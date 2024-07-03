from django.urls import path
from auxiliaries import views

# Create your URL configuration here.
urlpatterns = [
    path("public/service/map/", views.PublicServiceMap, name = "Public Service Map"),    

    path("public/service/resource/", views.PublicServiceResource, name = "Public Service Resource"),

    path("public/service/inquiry/", views.PublicServiceInquiry, name = "Public Service Inquiry"),

    path("contributor/service/map/", views.ContributorServiceMap, name = "Contributor Service Map"),

    path("contributor/service/resource/", views.ContributorServiceResource, name = "Contributor Service Resource"),

    path("contributor/service/inquiry/", views.ContributorServiceInquiry, name = "Contributor Service Inquiry"),

    path("service/link/read/<int:id>/redirect/", views.ServiceLinkReadRedirect, name = "Service Link Read Redirect"),

    path("service/file/read/<int:id>/redirect/", views.ServiceFileReadRedirect, name = "Service File Read Redirect"),    
]