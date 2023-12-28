from django.urls import path
from authentications import views

# Create your URL configuration here.
urlpatterns = [
    path("", views.PublicHome, name = "Public Home"),
    path("contributor/signup/", views.ContributorSignup, name = "Contributor Signup"),
    path("contributor/login/", views.ContributorSignin, name = "Contributor Signin"),
    path("contributor/home/", views.ContributorHome, name = "Contributor Home"),
    path("contributor/profile/", views.ContributorProfile, name = "Contributor Profile"),
    path("contributor/profile/update/", views.ContributorProfileUpdate, name = "Contributor Profile Update"),
    path("contributor/logout/", views.ContributorSignout, name = "Contributor Signout"),
    path("officer/signup/", views.OfficerSignup, name = "Officer Signup"),
    path("officer/login/", views.OfficerSignin, name = "Officer Signin"),
    path("officer/logout/", views.OfficerSignout, name = "Officer Signout"),
    path("admin/login/", views.AdministratorSignin, name = "Administrator Signin"),
    path("admin/logout/", views.AdministratorSignout, name = "Administrator Signout"),
]