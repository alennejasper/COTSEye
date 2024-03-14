from django.urls import path
from authentications import views

# Create your URL configuration here.
urlpatterns = [
    path("", views.PublicHome, name = "Public Home"),
    
    path("contributor/service/register/", views.ContributorServiceRegister, name = "Contributor Service Register"),
   
    path("contributor/service/login/", views.ContributorServiceLogin, name = "Contributor Service Login"),
    
    path("contributor/service/login/facebook/", views.ContributorServiceLoginFacebook, name = "Contributor Service Login Facebook"),
    
    path("contributor/service/login/google/", views.ContributorServiceLoginGoogle, name = "Contributor Service Login Google"),
    
    path("contributor/service/home/", views.ContributorServiceHome, name = "Contributor Service Home"),
    
    path("contributor/service/profile/", views.ContributorServiceProfile, name = "Contributor Service Profile"),
    
    path("contributor/service/profile/update/", views.ContributorServiceProfileUpdate, name = "Contributor Service Profile Update"),
    
    path("contributor/service/logout/", views.ContributorServiceLogout, name = "Contributor Service Logout"),
    
    path("officer/database/register/", views.OfficerDatabaseRegister, name = "Officer Database Register"),
    
    path("officer/database/login/", views.OfficerDatabaseLogin, name = "Officer Database Login"),
    
    path("contributor/login/facebook/", views.OfficerDatabaseLoginFacebook, name = "Officer Database Login Facebook"),
    
    path("contributor/login/google/", views.OfficerDatabaseLoginGoogle, name = "Officer Database Login Google"),
    
    path("officer/logout/", views.OfficerLogout, name = "Officer Logout"),
    
    path("admin/database/login/", views.AdministratorDatabaseLogin, name = "Administrator Database Login"),
    
    path("admin/database/logout/", views.AdministratorDatabaseLogout, name = "Administrator Database Logout"),
]