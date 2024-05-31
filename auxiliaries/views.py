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


import json

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

    municipality_filter = request.GET.get('municipality')
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')

    # Fetch distinct municipalities
    municipalities = Location.objects.values('municipality').distinct()

    # Fetch locations with optional filters
    locations_query = Location.objects.filter(status__isnull=False)
    if municipality_filter:
        locations_query = locations_query.filter(municipality=municipality_filter)

    locations = locations_query.distinct()

    data = {}
    total_caught_overall = 0

    barangay_data = []

    for location in locations:
        location_str = f"{location.barangay}, {location.municipality}"
        statuses_query = Status.objects.filter(location=location).order_by('onset_date')

        if start_date_filter and end_date_filter:
            statuses_query = statuses_query.filter(onset_date__range=[start_date_filter, end_date_filter])

        latest_status = statuses_query.latest('onset_date')
        caught_overall_sum = latest_status.caught_overall
        total_caught_overall += caught_overall_sum

        data[location_str] = {
            'onset_dates': [latest_status.onset_date.strftime('%Y-%m-%d')],
            'caught_overalls': [caught_overall_sum],
            'caught_overall_sum': caught_overall_sum
        }

        barangay_data.append({
            'barangay': location.barangay,
            'municipality': location.municipality,
            'caught_overall_sum': caught_overall_sum,
            'latest_onset_date': latest_status.onset_date.strftime('%Y-%m-%d')
        })

    try:
        map_posts = Post.objects.filter(post_status = 1)

        map_statuses = Status.objects.all()

        map_graphs = Status.objects.order_by("location", "-onset_date").distinct("location")[:5]

    except:
        map_posts = None

        map_statuses = None

        map_graphs = None

    context = {"username": username, "map_posts": map_posts, "map_statuses": map_statuses, "map_graphs": map_graphs,'chart_data': json.dumps(data),
        'locations': locations,
        'municipalities': municipalities,
        'total_caught_overall': total_caught_overall,
        'barangay_data': barangay_data,
        'selected_municipality': municipality_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter}
    
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

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    unread_posts = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:5]

    context = {"username": username, "user_profile": user_profile, "announcements": announcements, "unread_posts": unread_posts, "scheme": scheme, "host": host}

    return render(request, "contributor/service/announcement/announcement.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncementRead(request, id): 
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    announcement = Announcement.objects.get(id = id)

    unread_posts = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:5]

    context = {"username": username, "user_profile": user_profile, "scheme": scheme, "host": host, "announcement": announcement, "unread_posts": unread_posts}

    return render(request, "contributor/service/announcement/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceInquiry(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    inquiries = Inquiry.objects.all()

    unread_posts = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:5]

    context = {"username": username, "user_profile": user_profile, "inquiries": inquiries, "unread_posts": unread_posts}

    return render(request, "contributor/service/inquiry/inquiry.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceMap(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_posts = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:5]

    try:
        map_posts = Post.objects.filter(post_status = 1)

        map_statuses = Status.objects.all()

        map_graphs = Status.objects.order_by("location", "-onset_date").distinct("location")[:5]

    except:
        map_posts = None

        map_statuses = None

        map_graphs = None

    municipality_filter = request.GET.get('municipality')
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')

    # Fetch distinct municipalities
    municipalities = Location.objects.values('municipality').distinct()

    # Fetch locations with optional filters
    locations_query = Location.objects.filter(status__isnull=False)
    if municipality_filter:
        locations_query = locations_query.filter(municipality=municipality_filter)

    locations = locations_query.distinct()

    unread_posts = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:5]

    data = {}
    total_caught_overall = 0

    barangay_data = []

    for location in locations:
        location_str = f"{location.barangay}, {location.municipality}"
        statuses_query = Status.objects.filter(location=location).order_by('onset_date')

        if start_date_filter and end_date_filter:
            statuses_query = statuses_query.filter(onset_date__range=[start_date_filter, end_date_filter])

        latest_status = statuses_query.latest('onset_date')
        caught_overall_sum = latest_status.caught_overall
        total_caught_overall += caught_overall_sum

        data[location_str] = {
            'onset_dates': [latest_status.onset_date.strftime('%Y-%m-%d')],
            'caught_overalls': [caught_overall_sum],
            'caught_overall_sum': caught_overall_sum
        }

        barangay_data.append({
            'barangay': location.barangay,
            'municipality': location.municipality,
            'caught_overall_sum': caught_overall_sum,
            'latest_onset_date': latest_status.onset_date.strftime('%Y-%m-%d')
        })

    context = {"username": username, "user_profile": user_profile, "map_posts": map_posts, "map_statuses": map_statuses, "map_graphs": map_graphs, "unread_posts": unread_posts, 'chart_data': json.dumps(data),
        'locations': locations,
        'municipalities': municipalities,
        'total_caught_overall': total_caught_overall,
        'barangay_data': barangay_data,
        'selected_municipality': municipality_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter}

    return render(request, "contributor/service/map/map.html", context)

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceResource(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    resource_links = ResourceLink.objects.all()

    resource_files = ResourceFile.objects.all()

    unread_posts = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:5]
    
    context = {"username": username, "user_profile": user_profile, "resource_links": resource_links, "resource_files": resource_files, "unread_posts": unread_posts}
    
    return render(request, "contributor/service/resource/resource.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncement(request):
    notification_life = timezone.now() - timedelta(days = 30) 

    unread_posts = Post.objects.filter(read_status = False, creation_date__gte = notification_life).order_by("-creation_date")[:5]

    announcements = Announcement.objects.all().order_by('-release_date')

    locations = Location.objects.all()

    context = {"unread_posts": unread_posts, "announcements": announcements, "locations": locations}

    return render(request, "officer/control/announcement/announcement.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def officer_control_announcement(request, pk):
    notification_life = timezone.now() - timedelta(days = 30)

    unread_posts = Post.objects.filter(read_status = False, creation_date__gte = notification_life).order_by("-creation_date")[:5]

    announcement = get_object_or_404(Announcement, pk = pk)

    other_announcements = Announcement.objects.exclude(pk = pk)

    context = {"unread_posts": unread_posts, "announcement": announcement, "other_announcements": other_announcements}

    return render(request, "officer/control/announcement/specific_announcement.html", context)

@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def officercontroladdannouncement(request):
    notification_life = timezone.now() - timedelta(days = 30)

    unread_posts = Post.objects.filter(read_status = False, creation_date__gte = notification_life).order_by("-creation_date")[:5]

    locations = Location.objects.all().distinct("municipality")

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES)

        if form.is_valid():
            municipality = request.POST.get("municipality")

            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality = municipality, barangay = barangay)

                announcement = form.save(commit = False)

                announcement.location = location

                announcement.save()

            except Location.DoesNotExist:
                form.add_error(None, "The selected location does not exist.")

            return redirect("Officer Control Announcement")
        
    else:
        form = AnnouncementForm()

    context = {"unread_posts": unread_posts, "form": form, "locations": locations}

    return render(request, "officer/control/announcement/addannouncement.html", context)

@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def get_barangays(request):
    municipality = request.GET.get("municipality")

    barangays = Location.objects.filter(municipality = municipality).values_list("barangay", flat = True).distinct()

    return JsonResponse(list(barangays), safe = False)

@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def officercontrolupdateannouncement(request, pk):
    notification_life = timezone.now() - timedelta(days = 30)

    unread_posts = Post.objects.filter(read_status = False, creation_date__gte = notification_life).order_by("-creation_date")[:5]

    announcement = get_object_or_404(Announcement, pk = pk)

    locations = Location.objects.all().distinct("municipality")

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance = announcement)

        if form.is_valid():
            municipality = request.POST.get("municipality")

            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality = municipality, barangay = barangay)

                updated_announcement = form.save(commit = False)

                updated_announcement.location = location

                updated_announcement.save()

                return redirect("Officer Control Announcement")
            
            except Location.DoesNotExist:
                form.add_error(None, "The selected location does not exist.")

    else:
        form = AnnouncementForm(instance=announcement)
    
    context = {"unread_posts": unread_posts, "form": form, "announcement": announcement, "locations": locations}

    return render(request, "officer/control/announcement/updateannouncement.html", context)

@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def officercontroldeleteannouncement(request, pk):
    announcement = get_object_or_404(Announcement, pk = pk)

    if request.method == "DELETE":
        announcement.delete()

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})


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