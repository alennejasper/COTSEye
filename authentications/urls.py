from django.urls import path
from authentications import views

# Create your URL configuration here.
urlpatterns = [
    path("public/service/fallback/", views.PublicServiceFallback, name = "Public Service Fallback"),

    path("public/service/home/", views.PublicServiceHome, name = "Public Service Home"),
    
    path("contributor/service/fallback/", views.ContributorServiceFallback, name = "Contributor Service Fallback"),

    path("contributor/service/register/", views.ContributorServiceRegister, name = "Contributor Service Register"),
   
    path("contributor/service/login/", views.ContributorServiceLogin, name = "Contributor Service Login"),
            
    path("contributor/service/home/", views.ContributorServiceHome, name = "Contributor Service Home"),
    
    path("contributor/service/notification/", views.ContributorServiceNotification, name = "Contributor Service Notification"),

    path("contributor/service/notification/mark/<int:id>/", views.ContributorServiceNotificationMark, name = "Contributor Service Notification Mark"),

    path("contributor/notifications/read/<int:id>/", views.ContributorServiceMarkNotificationAsRead, name = "Contributor Service Notification Read"),

    path("contributor/service/profile/", views.ContributorServiceProfile, name = "Contributor Service Profile"),
    
    path("contributor/service/profile/update/", views.ContributorServiceProfileUpdate, name = "Contributor Service Profile Update"),

    path("contributor/service/profile/update/fetch/", views.ContributorServiceProfileUpdateFetch, name = "Contributor Service Profile Update Fetch"),

    path("officer/control/profile/delete/<int:id>/", views.ContributorServiceProfileDelete, name = "Contributor Service Profile Delete"),

    path("contributor/service/profile/delete/fetch/", views.ContributorServiceProfileDeleteFetch, name = "Contributor Service Profile Delete Fetch"),
    
    path("contributor/service/leaderboard/", views.ContributorServiceLeaderboard, name = "Contributor Service Leaderboard"),

    path("contributor/service/logout/", views.ContributorServiceLogout, name = "Contributor Service Logout"),       

    path("officer/control/fallback/", views.OfficerControlFallback, name = "Officer Control Fallback"),

    path("officer/control/register/", views.OfficerControlRegister, name = "Officer Control Register"),

    path("officer/control/login/", views.OfficerControlLogin, name = "Officer Control Login"),

    path("officer/control/home/", views.OfficerControlHome, name = "Officer Control Home"),

    path("officer/control/notification/", views.OfficerControlNotification, name = "Officer Control Notification"),

    path("officer/control/notification/mark/<int:id>/", views.OfficerControlNotificationMark, name = "Officer Control Notification Mark"),
    
    path("officer/control/notification/read/<int:id>/", views.OfficerControlMarkNotificationAsRead, name = "Officer Control Notification Read"),

    path("officer/control/profile/", views.OfficerControlProfile, name = "Officer Control Profile"),
    
    path("officer/control/profile/update/", views.OfficerControlProfileUpdate, name = "Officer Control Profile Update"),

    path("officer/control/profile/delete/<int:id>/", views.OfficerControlProfileDelete, name = "Officer Control Profile Delete"),

    path("officer/control/logout/", views.OfficerControlLogout, name = "Officer Control Logout"),      
]