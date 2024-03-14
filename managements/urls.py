from django.urls import path
from managements import views

# Create your URL configuration here.
urlpatterns = [
    path("public/service/status/", views.PublicServiceStatus, name = "Public Service Status"),

    path("contributor/service/status/", views.ContributorServiceStatus, name = "Contributor Service Status"),

    path("public/service/intervention/", views.PublicServiceIntervention, name = "Public Service Intervention"),

    path("intervention/service/read/<int:id>", views.PublicServiceInterventionRead, name = "Public Service Intervention Read"),

    path("contributor/service/intervention/", views.ContributorServiceIntervention, name = "Contributor Service Intervention"),

    path("contributor/service/intervention/read/<int:id>", views.ContributorServiceInterventionRead, name = "Contributor Service Intervention Read")
]