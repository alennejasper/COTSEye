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

    path("officer/report/register/", views.OfficerReportRegister, name = "Officer Report Register"),
    
    path("officer/report/login/", views.OfficerReportLogin, name = "Officer Report Login"),
    
    path("officer/report/login/facebook/", views.OfficerReportLoginFacebook, name = "Officer Report Login Facebook"),
    
    path("officer/report/login/google/", views.OfficerReportLoginGoogle, name = "Officer Report Login Google"),

    path("officer/report/home/redirect/", views.OfficerReportHomeRedirect, name = "Officer Report Home Redirect"),

    path("officer/report/profile/redirect/<int:id>/", views.OfficerReportProfileRedirect, name = "Officer Report Profile Redirect"),
    
    path("officer/report/logout/", views.OfficerReportLogout, name = "Officer Report Logout"),

    path("admin/report/login/", views.AdministratorReportLogin, name = "Administrator Report Login"),

    path("admin/report/home/", views.AdministratorReportHome, name = "Administrator Report Home"),

    path("admin/report/home/redirect/", views.AdministratorReportHomeRedirect, name = "Administrator Report Home Redirect"),

    path("admin/report/profile/redirect/<int:id>/", views.AdministratorReportProfileRedirect, name = "Administrator Report Profile Redirect"),

    path("admin/report/logout/", views.AdministratorReportLogout, name = "Administrator Report Logout"),
]