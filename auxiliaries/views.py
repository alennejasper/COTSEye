from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.encoding import smart_str
from auxiliaries.models import *
from authentications.views import OfficerCheck, ContributorCheck
from managements.models import Status
from reports.models import Post
from auxiliaries.forms import AnnouncementForm
from django.http import JsonResponse


import datetime
import json

# Create your views here.
def PublicServiceAnnouncement(request):
    username = "public/everyone"

    locations = Location.objects.all()

    municipalities = Location.objects.values("municipality").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    announcements = Announcement.objects.all().order_by("-release_date")

    if municipality:
        announcements = announcements.filter(location__municipality = municipality)

    if barangay:
        announcements = announcements.filter(location__barangay = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        announcements = announcements.filter(release_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        announcements = announcements.filter(release_date__lte = to_date)

    context = {"username": username, "locations": locations, "municipalities": municipalities, "announcements": announcements}

    return render(request, "public/service/announcement/announcement.html", context)


def PublicServiceAnnouncementRead(request, id):
    username = "public/everyone"

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    announcement = Announcement.objects.get(id = id)

    context = {"username": username, "scheme": scheme, "host": host, "announcement": announcement}

    return render(request, "public/service/announcement/read.html", context)


def PublicServiceInquiry(request):
    username = "public/everyone"

    inquiries = Inquiry.objects.all()

    context = {"username": username, "inquiries": inquiries}

    return render(request, "public/service/inquiry/inquiry.html", context)


def PublicServiceMap(request):
    username = "public/everyone"

    try:
        map_posts = Post.objects.filter(post_status = 1)

        map_statuses = Status.objects.all()

    except:
        map_posts = None

        map_statuses = None

    context = {"username": username, "map_posts": map_posts, "map_statuses": map_statuses}
    
    return render(request, "public/service/map/map.html", context)


def PublicServiceResource(request):
    username = "public/everyone"

    resource_links = Link.objects.all()

    resource_files = File.objects.all()
    
    context = {"username": username, "resource_links": resource_links, "resource_files": resource_files}
    
    return render(request, "public/service/resource/resource.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncement(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    locations = Location.objects.all()

    municipalities = Location.objects.values("municipality").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    announcements = Announcement.objects.all().order_by("-release_date")

    if municipality:
        announcements = announcements.filter(location__municipality = municipality)

    if barangay:
        announcements = announcements.filter(location__barangay = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        announcements = announcements.filter(release_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        announcements = announcements.filter(release_date__lte = to_date)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "locations": locations, "municipalities": municipalities, "announcements": announcements}

    return render(request, "contributor/service/announcement/announcement.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncementRead(request, id): 
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    announcement = Announcement.objects.get(id = id)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "scheme": scheme, "host": host, "announcement": announcement}

    return render(request, "contributor/service/announcement/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceInquiry(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    inquiries = Inquiry.objects.all()

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "inquiries": inquiries}

    return render(request, "contributor/service/inquiry/inquiry.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceMap(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    try:
        map_posts = Post.objects.filter(post_status = 1)

        map_statuses = Status.objects.all()

    except:
        map_posts = None

        map_statuses = None

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "map_posts": map_posts, "map_statuses": map_statuses}

    return render(request, "contributor/service/map/map.html", context)

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceResource(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    resource_links = Link.objects.all()

    resource_files = File.objects.all()
    
    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "resource_links": resource_links, "resource_files": resource_files}
    
    return render(request, "contributor/service/resource/resource.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncement(request):
    notification_life = timezone.now() - timedelta(days = 30) 

    unread_notifications = Post.objects.filter(read_status = False, creation_date__gte = notification_life).order_by("-creation_date")[:5]

    announcements = Announcement.objects.all().order_by('-release_date')

    municipalities = Location.objects.values('municipality').distinct()

    locations = Location.objects.all()

    context = {"unread_notifications": unread_notifications, "announcements": announcements, 'municipalities': municipalities, "locations": locations}

    return render(request, "officer/control/announcement/announcement.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def officer_control_announcement(request, pk):
    notification_life = timezone.now() - timedelta(days = 30)

    unread_notifications = Post.objects.filter(read_status = False, creation_date__gte = notification_life).order_by("-creation_date")[:5]

    announcement = get_object_or_404(Announcement, pk = pk)

    other_announcements = Announcement.objects.exclude(pk = pk)

    announcements = Announcement.objects.all().order_by('-release_date')

    municipalities = Location.objects.values('municipality').distinct()

    context = {"unread_notifications": unread_notifications, "announcement": announcement, 'municipalities': municipalities, "other_announcements": other_announcements}

    return render(request, "officer/control/announcement/specific_announcement.html", context)

@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def officercontroladdannouncement(request):
    notification_life = timezone.now() - timedelta(days=30)

    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by("-creation_date")[:5]

    locations = Location.objects.all().distinct("municipality")
    municipalities = Location.objects.values('municipality').distinct()

    errors = None
    field_labels = None
    location_error = None

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, user=request.user.user)

        if form.is_valid():
            municipality = request.POST.get("municipality")
            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality=municipality, barangay=barangay)

                announcement = form.save(commit=False)
                announcement.location = location
                announcement.save()

                return redirect("Officer Control Announcement")

            except Location.DoesNotExist:
                location_error = "The selected location does not exist."

        errors = form.errors.as_json()
        field_labels = {field.name: field.label for field in form}

    else:
        form = AnnouncementForm()

    context = {
        "unread_notifications": unread_notifications,
        "form": form,
        "municipalities": municipalities,
        "locations": locations,
        "errors": errors,
        "field_labels": field_labels,
        "location_error": location_error
    }

    return render(request, "officer/control/announcement/addannouncement.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def get_barangays(request):
    municipality = request.GET.get("municipality")

    barangays = Location.objects.filter(municipality = municipality).values_list("barangay", flat = True).distinct()

    return JsonResponse(list(barangays), safe = False)

@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def officercontrolupdateannouncement(request, pk):
    notification_life = timezone.now() - timedelta(days=30)

    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by("-creation_date")[:5]

    announcement = get_object_or_404(Announcement, pk=pk)

    municipalities = Location.objects.values('municipality').distinct()
    locations = Location.objects.all().distinct("municipality")

    errors = None
    field_labels = None
    location_error = None

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)

        if form.is_valid():
            municipality = request.POST.get("municipality")
            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality=municipality, barangay=barangay)

                updated_announcement = form.save(commit=False)
                updated_announcement.location = location
                updated_announcement.save()

                return redirect("Officer Control Announcement")

            except Location.DoesNotExist:
                location_error = "The selected location does not exist."

        errors = form.errors.as_json()
        field_labels = {field.name: field.label for field in form}

    else:
        form = AnnouncementForm(instance=announcement)

    context = {
        "unread_notifications": unread_notifications,
        "form": form,
        "announcement": announcement,
        "municipalities": municipalities,
        "locations": locations,
        "errors": errors,
        "field_labels": field_labels,
        "location_error": location_error
    }

    return render(request, "officer/control/announcement/updateannouncement.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def officercontroldeleteannouncement(request, pk):
    announcement = get_object_or_404(Announcement, pk = pk)

    if request.method == "DELETE":
        announcement.delete()

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})


def ServiceLinkReadRedirect(request, id):
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            try:
                resource_link = Link.objects.get(id = id).resource_link
            
            except:
                resource_link = ""

            return redirect(resource_link)
    
    else:
        try:
            resource_link = Link.objects.get(id = id).resource_link
            
        except:
            resource_link = ""

        return redirect(resource_link)
    

def ServiceFileReadRedirect(request, id):
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            try:
                resource_file = File.objects.get(id = id).resource_file
            
            except:
                resource_file = ""

        filename = resource_file.name.replace("_", " ")

        return FileResponse(open(resource_file.path, "rb"), as_attachment = True, filename = smart_str(filename))
        
    else:
        try:
            resource_file = File.objects.get(id = id).resource_file
            
        except:
            resource_file = ""

        filename = resource_file.name.replace("_", " ")

        return FileResponse(open(resource_file.path, "rb"), as_attachment = True, filename = smart_str(filename))