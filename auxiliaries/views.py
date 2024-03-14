from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from auxiliaries.models import *
from authentications.views import ContributorCheck

# Create your views here.
def PublicServiceAnnouncement(request):
    username = "public/everyone"

    announcements = Announcement.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        if "from_date" in request.GET or "to_date" in request.GET:
            if from_date and to_date:
                announcements = Announcement.objects.filter(release_date__range = [from_date, to_date])
            
                if not announcements:
                    username = "public/everyone"

                    messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

            elif not from_date and not to_date:
                messages.error(request, "Range is not valid.")

            elif not from_date or not to_date:
                messages.error(request, "Range is not valid.")

        elif not announcements:
            username = "public/everyone"

            messages.error(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "announcements": announcements}

    return render(request, "public/service/announcement/announcement.html", context)


def PublicServiceAnnouncementRead(request, id):
    username = "public/everyone"

    announcement = Announcement.objects.filter(id = id)

    context = {"username": username, "announcement": announcement}

    return render(request, "public/service/announcement/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncement(request):
    username = request.user.username

    announcements = Announcement.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        if "from_date" in request.GET or "to_date" in request.GET:
            if from_date and to_date:
                announcements = Announcement.objects.filter(release_date__range = [from_date, to_date])
            
                if not announcements:
                    username = request.user.username

                    messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

            elif not from_date and not to_date:
                messages.error(request, "Range is not valid.")

            elif not from_date or not to_date:
                messages.error(request, "Range is not valid.")

        elif not announcements:
            username = request.user.username

            messages.error(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "announcements": announcements}

    return render(request, "contributor/service/announcement/announcement.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncementRead(request, id): 
    username = request.user.username

    announcement = Announcement.objects.filter(id = id)

    context = {"username": username, "announcement": announcement}

    return render(request, "contributor/service/announcement/read.html", context)