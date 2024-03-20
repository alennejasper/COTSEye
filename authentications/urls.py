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
]