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

    path("contributor/service/profile/delete/<int:id>/", views.ContributorServiceProfileDelete, name = "Contributor Service Profile Delete"),

    path("contributor/service/profile/delete/fetch/", views.ContributorServiceProfileDeleteFetch, name = "Contributor Service Profile Delete Fetch"),
    
    path("contributor/service/leaderboard/", views.ContributorServiceLeaderboard, name = "Contributor Service Leaderboard"),

    path("contributor/service/logout/", views.ContributorServiceLogout, name = "Contributor Service Logout"),       

    path("curator/control/fallback/", views.CuratorControlFallback, name = "Curator Control Fallback"),

    path("curator/control/register/", views.CuratorControlRegister, name = "Curator Control Register"),

    path("curator/control/login/", views.CuratorControlLogin, name = "Curator Control Login"),

    path("curator/control/home/", views.CuratorControlHome, name = "Curator Control Home"),

    path("curator/control/notification/", views.CuratorControlNotification, name = "Curator Control Notification"),

    path("curator/control/notification/mark/<int:id>/", views.CuratorControlNotificationMark, name = "Curator Control Notification Mark"),
    
    path("curator/control/notification/read/<int:id>/", views.CuratorControlNotificationRead, name = "Curator Control Notification Read"),

    path("curator/control/profile/", views.CuratorControlProfile, name = "Curator Control Profile"),
    
    path("curator/control/profile/update/", views.CuratorControlProfileUpdate, name = "Curator Control Profile Update"),

    path("curator/control/profile/delete/<int:id>/", views.CuratorControlProfileDelete, name = "Curator Control Profile Delete"),

    path("curator/control/logout/", views.CuratorControlLogout, name = "Curator Control Logout"),      
]