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
    
    path("officer/database/login/facebook/", views.OfficerDatabaseLoginFacebook, name = "Officer Database Login Facebook"),
    
    path("officer/database/login/google/", views.OfficerDatabaseLoginGoogle, name = "Officer Database Login Google"),
    
    path("officer/database/logout/", views.OfficerDatabaseLogout, name = "Officer Database Logout"),
    
    path("admin/database/login/", views.AdministratorDatabaseLogin, name = "Administrator Database Login"),
    
    path("admin/database/logout/", views.AdministratorDatabaseLogout, name = "Administrator Database Logout"),

    path("officer/statistics/register/", views.OfficerStatisticsRegister, name = "Officer Statistics Register"),
    
    path("officer/statistics/login/", views.OfficerStatisticsLogin, name = "Officer Statistics Login"),
    
    path("officer/statistics/login/facebook/", views.OfficerStatisticsLoginFacebook, name = "Officer Statistics Login Facebook"),
    
    path("officer/statistics/login/google/", views.OfficerStatisticsLoginGoogle, name = "Officer Statistics Login Google"),

    path("officer/statistics/home/", views.OfficerStatisticsHome, name = "Officer Statistics Home"),

    path("officer/statistics/home/redirect/", views.OfficerStatisticsHomeRedirect, name = "Officer Statistics Home Redirect"),

    path("officer/statistics/password/redirect/", views.OfficerStatisticsPasswordRedirect, name = "Officer Statistics Password Redirect"),

    path("officer/statistics/profile/redirect/", views.OfficerStatisticsProfileRedirect, name = "Officer Statistics Profile Redirect"),
    
    path("officer/statistics/logout/", views.OfficerStatisticsLogout, name = "Officer Statistics Logout"),

    path("admin/statistics/login/", views.AdministratorStatisticsLogin, name = "Administrator Statistics Login"),

    path("admin/statistics/home/", views.AdministratorStatisticsHome, name = "Administrator Statistics Home"),

    path("admin/statistics/home/redirect/", views.AdministratorStatisticsHomeRedirect, name = "Administrator Statistics Home Redirect"),

    path("admin/statistics/password/redirect/", views.AdministratorStatisticsPasswordRedirect, name = "Administrator Statistics Password Redirect"),

    path("admin/statistics/profile/redirect/", views.AdministratorStatisticsProfileRedirect, name = "Administrator Statistics Profile Redirect"),

    path("admin/statistics/logout/", views.AdministratorStatisticsLogout, name = "Administrator Statistics Logout"),
]