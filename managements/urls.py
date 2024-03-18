from django.urls import path
from managements import views

# Create your URL configuration here.
urlpatterns = [
    path("service/status/", views.PublicServiceStatus, name = "Public Service Status"),

    path("service/intervention/", views.PublicServiceIntervention, name = "Public Service Intervention"),

    path("service/intervention/read/<int:id>/", views.PublicServiceInterventionRead, name = "Public Service Intervention Read"),

    path("contributor/service/status/", views.ContributorServiceStatus, name = "Contributor Service Status"),

    path("contributor/service/intervention/", views.ContributorServiceIntervention, name = "Contributor Service Intervention"),

    path("contributor/service/intervention/read/<int:id>/", views.ContributorServiceInterventionRead, name = "Contributor Service Intervention Read"),

    path("officer/statistics/intervention/", views.OfficerStatisticsIntervention, name = "Officer Statistics Intervention"),

    path("officer/statistics/intervention/read/<int:id>/", views.OfficerStatisticsInterventionRead, name = "Officer Statistics Intervention Read"),

    path("officer/statistics/status/", views.OfficerStatisticsStatus, name = "Officer Statistics Status"),

    path("admin/statistics/intervention/", views.AdministratorStatisticsIntervention, name = "Administrator Statistics Intervention"),

    path("admin/statistics/intervention/read/<int:id>/", views.AdministratorStatisticsInterventionRead, name = "Administrator Statistics Intervention Read"),

    path("admin/statistics/status/", views.AdministratorStatisticsStatus, name = "Administrator Statistics Status"),
]