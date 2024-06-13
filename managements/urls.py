from django.urls import path
from managements import views

# Create your URL configuration here.
urlpatterns = [
    path("public/service/intervention/", views.PublicServiceIntervention, name = "Public Service Intervention"),

    path("public/service/intervention/read/<int:id>/", views.PublicServiceInterventionRead, name = "Public Service Intervention Read"),

    path("contributor/service/intervention/", views.ContributorServiceIntervention, name = "Contributor Service Intervention"),

    path("contributor/service/intervention/read/<int:id>/", views.ContributorServiceInterventionRead, name = "Contributor Service Intervention Read"),

    path("officer/control/intervention/", views.OfficerControlIntervention, name = "Officer Control Intervention"),

    path('officer/control/intervention/add/', views.OfficerControlInterventionAdd, name='Officer Control Intervention Add'),

    path('officer/control/intervention/update/<int:pk>/', views.OfficerControlInterventionUpdate, name='Officer Control Intervention Update'),

    path('officer/control/intervention/delete/<int:pk>/', views.OfficerControlInterventionDelete, name='Officer Control Intervention Delete'),

    path('officer/control/intervention/detail/<int:pk>/', views.OfficerControlInterventionDetail, name='Officer Control Intervention Detail'),

    path("officer/control/status/", views.OfficerControlStatus, name = "Officer Control Status"),

    path("officer/control/status/add", views.OfficerControlStatusAdd, name = "Officer Control Status Add"),

    path("officer/control/status/delete/<int:status_id>", views.OfficerControlDeleteStatus, name = "Officer Control Status Delete"),

    path("officer/control/report/", views.OfficerControlReport, name = "Officer Control Report"),

    path('municipality/<str:municipality_name>/', views.BarangayStatusView, name='barangay_status'),

    path('barangay/<str:barangay_name>/', views.BarangayAllStatusesView, name='barangay_all_statuses'),

   
]