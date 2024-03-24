from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from auxiliaries.models import *
from authentications.views import ContributorCheck

# Create your views here.
def PublicServiceAnnouncement(request):
    username = "public/everyone"

    records = Announcement.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        results = None

        if from_date and to_date:
            results = Announcement.objects.filter(release_date__range = [from_date, to_date])
        
        elif not from_date or not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.") 
        
        elif from_date and to_date and to_date < from_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")

        if results is None:
            username = "public/everyone"

            messages.info(request, username + ", " + "kindly filter announcements within COTSEye to check for updates today.")

        elif not results:
            username = "public/everyone"

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results}

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

    records = Announcement.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        results = None

        if from_date and to_date:
            results = Announcement.objects.filter(release_date__range = [from_date, to_date])

        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date or not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 

        elif not from_date and not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter announcements within COTSEye to check for updates today.")

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results}

    return render(request, "contributor/service/announcement/announcement.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncementRead(request, id): 
    username = request.user.username

    announcement = Announcement.objects.filter(id = id)

    context = {"username": username, "announcement": announcement}

    return render(request, "contributor/service/announcement/read.html", context)