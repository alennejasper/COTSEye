from django.urls import path
from managements import views

# Create your URL configuration here.
urlpatterns = [
    path("public/status/", views.PublicStatus, name = "Public Status"),

    path("contributor/status/", views.ContributorStatus, name = "Contributor Status"),

    path("intervention/", views.PublicIntervention, name = "Public Intervention"),

    path("intervention/read/<int:id>", views.PublicInterventionRead, name = "Public Intervention Read"),

    path("contributor/intervention/", views.ContributorIntervention, name = "Contributor Intervention"),

    path("contributor/intervention/read/<int:id>", views.ContributorInterventionRead, name = "Contributor Intervention Read")
]