from django.urls import path
from authentications import views

# Create your URL configuration here.
urlpatterns = [
    path("", views.PublicHome, name = "Public Home"),
    path("contributor/signup/", views.ContributorSignup, name = "Contributor Signup"),
    path("contributor/login/", views.ContributorLogin, name = "Contributor Login"),
    path("contributor/login/facebook/", views.ContributorLoginFacebook, name = "Contributor Login Facebook"),
    path("contributor/login/google/", views.ContributorLoginGoogle, name = "Contributor Login Google"),
    path("contributor/home/", views.ContributorHome, name = "Contributor Home"),
    path("contributor/profile/", views.ContributorProfile, name = "Contributor Profile"),
    path("contributor/profile/update/", views.ContributorProfileUpdate, name = "Contributor Profile Update"),
    path("contributor/logout/", views.ContributorLogout, name = "Contributor Logout"),
    path("officer/signup/", views.OfficerSignup, name = "Officer Signup"),
    path("officer/login/", views.OfficerLogin, name = "Officer Login"),
    path("contributor/login/facebook/", views.OfficerLoginFacebook, name = "Officer Login Facebook"),
    path("contributor/login/google/", views.OfficerLoginGoogle, name = "Officer Login Google"),
    path("officer/logout/", views.OfficerLogout, name = "Officer Logout"),
    path("admin/login/", views.AdministratorLogin, name = "Administrator Login"),
    path("admin/logout/", views.AdministratorLogout, name = "Administrator Logout"),
]