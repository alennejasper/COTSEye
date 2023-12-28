from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from auxiliaries.models import *
from authentications.views import ContributorCheck

# Create your views here.
def PublicAnnouncement(request):
    announcements = Announcement.objects.all()

    context = {"announcements": announcements}
    return render(request, "public/announcement.html", context)


def PublicAnnouncementRead(request, id):
    announcements = Announcement.objects.filter(id = id)

    context = {"announcements": announcements}
    return render(request, "public/read.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorAnnouncement(request):
    announcements = Announcement.objects.all()

    context = {"announcements": announcements}
    return render(request, "contributor/announcement.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorAnnouncementRead(request, id): 
    announcements = Announcement.objects.filter(id = id)

    context = {"announcements": announcements}
    return render(request, "contributor/read.html", context)