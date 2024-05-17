from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Max
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import smart_str
from auxiliaries.models import *
from authentications.views import ContributorCheck
from managements.models import Status
from reports.models import Post
from auxiliaries.forms import AnnouncementForm
from django.http import JsonResponse


# Create your views here.
def PublicServiceAnnouncement(request):
    username = "public/everyone"

    announcements = Announcement.objects.all().order_by("-release_date")

    context = {"username": username, "announcements": announcements}

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

        map_graphs = Status.objects.order_by("location", "-onset_date").distinct("location")[:5]

    except:
        map_posts = None

        map_statuses = None

        map_graphs = None

    context = {"username": username, "map_posts": map_posts, "map_statuses": map_statuses, "map_graphs": map_graphs}
    
    return render(request, "public/service/map/map.html", context)


def PublicServiceResource(request):
    username = "public/everyone"

    resource_links = ResourceLink.objects.all()

    resource_files = ResourceFile.objects.all()
    
    context = {"username": username, "resource_links": resource_links, "resource_files": resource_files}
    
    return render(request, "public/service/resource/resource.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncement(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    announcements = Announcement.objects.all().order_by("-release_date")

    context = {"username": username, "user_profile": user_profile, "announcements": announcements}

    return render(request, "contributor/service/announcement/announcement.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncementRead(request, id): 
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    announcement = Announcement.objects.get(id = id)

    context = {"username": username, "user_profile": user_profile, "scheme": scheme, "host": host, "announcement": announcement}

    return render(request, "contributor/service/announcement/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceInquiry(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    inquiries = Inquiry.objects.all()

    context = {"username": username, "user_profile": user_profile, "inquiries": inquiries}

    return render(request, "contributor/service/inquiry/inquiry.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceMap(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    try:
        map_posts = Post.objects.filter(post_status = 1)

        map_statuses = Status.objects.all()

        map_graphs = Status.objects.order_by("location", "-onset_date").distinct("location")[:5]

    except:
        map_posts = None

        map_statuses = None

        map_graphs = None

    context = {"username": username, "user_profile": user_profile, "map_posts": map_posts, "map_statuses": map_statuses, "map_graphs": map_graphs}

    return render(request, "contributor/service/map/map.html", context)


def ContributorServiceResource(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    resource_links = ResourceLink.objects.all()

    resource_files = ResourceFile.objects.all()
    
    context = {"username": username, "user_profile": user_profile, "resource_links": resource_links, "resource_files": resource_files}
    
    return render(request, "contributor/service/resource/resource.html", context)


def OfficerControlAnnouncement(request):
    announcements = Announcement.objects.all()

    context = {"announcements": announcements}

    return render(request, "officer/control/announcement/announcement.html", context)


def officer_control_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    other_announcements = Announcement.objects.exclude(pk=pk)
    return render(request, "officer/control/announcement/specific_announcement.html", {
        'announcement': announcement,
        'other_announcements': other_announcements
    })
def officercontroladdannouncement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Officer Control Announcement')  # Redirect to the list of announcements or wherever you want
    else:
        form = AnnouncementForm()
    return render(request, "officer/control/announcement/addannouncement.html", {'form': form})

def officercontrolupdateannouncement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('Officer Control Announcement')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, "officer/control/announcement/updateannouncement.html", {'form': form, 'announcement': announcement})

def officercontroldeleteannouncement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'DELETE':
        announcement.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def ServiceResourceLinkReadRedirect(request, id):
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            try:
                resource_link = ResourceLink.objects.get(id = id).resource_link
            
            except:
                resource_link = ""

            return redirect(resource_link)
    
    else:
        try:
            resource_link = ResourceLink.objects.get(id = id).resource_link
            
        except:
            resource_link = ""

        return redirect(resource_link)
    

def ServiceResourceFileReadRedirect(request, id):
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            try:
                resource_file = ResourceFile.objects.get(id = id).resource_file
            
            except:
                resource_file = ""

        filename = resource_file.name.replace("_", " ")

        return FileResponse(open(resource_file.path, "rb"), as_attachment = True, filename = smart_str(filename))
        
    else:
        try:
            resource_file = ResourceFile.objects.get(id = id).resource_file
            
        except:
            resource_file = ""

        filename = resource_file.name.replace("_", " ")

        return FileResponse(open(resource_file.path, "rb"), as_attachment = True, filename = smart_str(filename))