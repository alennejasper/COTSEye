from django.urls import path
from managements import views

# Create your URL configuration here.
urlpatterns = [
    path("public/service/intervention/", views.PublicServiceIntervention, name = "Public Service Intervention"),

    path("public/service/intervention/read/<int:id>/", views.PublicServiceInterventionRead, name = "Public Service Intervention Read"),

    path("contributor/service/intervention/", views.ContributorServiceIntervention, name = "Contributor Service Intervention"),

    path("contributor/service/intervention/read/<int:id>/", views.ContributorServiceInterventionRead, name = "Contributor Service Intervention Read"),

    path("officer/control/intervention/", views.OfficerControlIntervention, name = "Officer Control Intervention"),

    path("officer/control/status/", views.OfficerControlStatus, name = "Officer Control Status"),

    path("officer/control/report/", views.OfficerControlReport, name = "Officer Control Report"),
]