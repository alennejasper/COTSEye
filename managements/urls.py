from django.urls import path
from managements import views

# Create your URL configuration here.
urlpatterns = [
    path("public/status/", views.PublicStatus, name = "Public Status"),

    path("contributor/status/", views.ContributorStatus, name = "Contributor Status")
]