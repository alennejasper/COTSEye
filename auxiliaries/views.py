from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from auxiliaries.models import *
from authentications.views import ContributorCheck

# Create your views here.
def PublicAnnouncement(request):
    announcements = Announcement.objects.all()

    context = {"announcements": announcements}

    return render(request, "public/announcement/announcement.html", context)


def PublicAnnouncementRead(request, id):
    announcement = Announcement.objects.filter(id = id)

    context = {"announcement": announcement}

    return render(request, "public/announcement/read.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorAnnouncement(request):
    announcements = Announcement.objects.all()

    context = {"announcements": announcements}

    return render(request, "contributor/announcement/announcement.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorAnnouncementRead(request, id): 
    announcement = Announcement.objects.filter(id = id)

    context = {"announcement": announcement}

    return render(request, "contributor/announcement/read.html", context)