from django.urls import path
from authentications import views

# Create your URL configuration here.
urlpatterns = [
    path("service/home/", views.PublicHome, name = "Public Home"),
    
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
    
    path("officer/database/login/facebook/", views.OfficerDatabaseLoginFacebook, name = "Officer Database Login Facebook"),
    
    path("officer/database/login/google/", views.OfficerDatabaseLoginGoogle, name = "Officer Database Login Google"),
    
    path("officer/database/logout/", views.OfficerDatabaseLogout, name = "Officer Database Logout"),
    
    path("admin/database/login/", views.AdministratorDatabaseLogin, name = "Administrator Database Login"),
    
    path("admin/database/logout/", views.AdministratorDatabaseLogout, name = "Administrator Database Logout"),
            
    path("database/home/redirect/", views.DatabaseHomeRedirect, name = "Database Home Redirect"),

    path("officer/statistics/home/", views.OfficerStatisticsHome, name = "Officer Statistics Home"),
    
    path("admin/statistics/home/", views.AdministratorStatisticsHome, name = "Administrator Statistics Home"),

    path("statistics/home/redirect/", views.StatisticsHomeRedirect, name = "Statistics Home Redirect"),

    path("statistics/password/redirect/", views.StatisticsPasswordRedirect, name = "Statistics Password Redirect"),

    path("statistics/profile/redirect/", views.StatisticsProfileRedirect, name = "Statistics Profile Redirect"),
]