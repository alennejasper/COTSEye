from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from authentications.views import ContributorCheck
from auxiliaries.models import *
from authentications.models import User, Notification
from managements.models import Status
from reports.models import Post
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.
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


def PublicServiceInquiry(request):
    username = "public/everyone"

    inquiries = Inquiry.objects.all()

    context = {"username": username, "inquiries": inquiries}

    return render(request, "public/service/inquiry/inquiry.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceMap(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days=30)

    user = User.objects.get(account=request.user)
    unread_notifications = Notification.objects.filter(user=user, is_read=False, creation_date__gte=notification_life).order_by("-creation_date")

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

    notification_life = timezone.now() - timedelta(days=30)

    user = User.objects.get(account=request.user)
    unread_notifications = Notification.objects.filter(user=user, is_read=False, creation_date__gte=notification_life).order_by("-creation_date")

    resource_links = Link.objects.all()

    resource_files = File.objects.all()
    
    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "resource_links": resource_links, "resource_files": resource_files}
    
    return render(request, "contributor/service/resource/resource.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceInquiry(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days=30)

    user = User.objects.get(account=request.user)
    unread_notifications = Notification.objects.filter(user=user, is_read=False, creation_date__gte=notification_life).order_by("-creation_date")

    inquiries = Inquiry.objects.all()

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "inquiries": inquiries}

    return render(request, "contributor/service/inquiry/inquiry.html", context)


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