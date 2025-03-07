from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from .forms import *
from .models import *
from authentications.models import User, Notification
from authentications.views import ContributorCheck, CuratorCheck
from django.utils import timezone
import datetime
import json
from django.db.models import Count


# Create your views here.
def PublicServiceAnnouncement(request):
    username = "public/everyone"

    locations = Location.objects.all()

    municipalities = Municipality.objects.values("municipality_name").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    announcements = Announcement.objects.all().order_by("-event_date")

    if municipality:
        announcements = announcements.filter(location__municipality__municipality_name = municipality)

    if barangay:
        announcements = announcements.filter(location__barangay__barangay_name = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        announcements = announcements.filter(event_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        announcements = announcements.filter(event_date__lte = to_date)

    context = {"username": username, "locations": locations, "municipalities": municipalities, "announcements": announcements}

    return render(request, "public/service/announcement/announcement.html", context)


def PublicServiceAnnouncementRead(request, id):
    username = "public/everyone"

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    announcement = Announcement.objects.get(id = id)

    context = {"username": username, "scheme": scheme, "host": host, "announcement": announcement}

    return render(request, "public/service/announcement/read.html", context)


def PublicServiceActivity(request):
    username = "public/everyone"

    locations = Location.objects.all()

    municipalities = Municipality.objects.values("municipality_name").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    activities = Activity.objects.all().order_by("-activity_date")

    if municipality:
        activities = activities.filter(location__municipality__municipality_name = municipality)

    if barangay:
        activities = activities.filter(location__barangay__barangay_name = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        activities = activities.filter(activity_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        activities = activities.filter(activity_date__lte = to_date)

    context = {"username": username, "locations": locations, "municipalities": municipalities, "activities": activities}

    return render(request, "public/service/activity/activity.html", context)


def PublicServiceActivityRead(request, id):
    username = "public/everyone"

    scheme = request.scheme

    host = request.META["HTTP_HOST"]
    
    activity = Activity.objects.get(id = id)

    context = {"username": username, "scheme": scheme, "host": host, "activity": activity}

    return render(request, "public/service/activity/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncement(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    locations = Location.objects.all()

    municipalities = Municipality.objects.values("municipality_name").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    announcements = Announcement.objects.all().order_by("-event_date")

    if municipality:
        announcements = announcements.filter(location__municipality__municipality_name = municipality)

    if barangay:
        announcements = announcements.filter(location__barangay__barangay_name = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        announcements = announcements.filter(event_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        announcements = announcements.filter(event_date__lte = to_date)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "locations": locations, "municipalities": municipalities, "announcements": announcements}

    return render(request, "contributor/service/announcement/announcement.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncementRead(request, id): 
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    announcement = Announcement.objects.get(id = id)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "scheme": scheme, "host": host, "announcement": announcement}

    return render(request, "contributor/service/announcement/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceActivity(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    locations = Location.objects.all()

    municipalities = Municipality.objects.values("municipality_name").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    activities = Activity.objects.all().order_by("-activity_date")

    if municipality:
        activities = activities.filter(location__municipality__municipality_name = municipality)

    if barangay:
        activities = activities.filter(location__barangay__barangay_name = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        activities = activities.filter(activity_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        activities = activities.filter(activity_date__lte = to_date)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "locations": locations, "municipalities": municipalities, "activities": activities}

    return render(request, "contributor/service/activity/activity.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceActivityRead(request, id):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    activity = Activity.objects.get(id = id)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "scheme": scheme, "host": host, "activity": activity}

    return render(request, "contributor/service/activity/read.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlAnnouncement(request):
    tab_number = 5

    announcement_number = 1

    notification_life = timezone.now() - timedelta(days = 30) 

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
   
    announcements = Announcement.objects.all().order_by("-event_date")

    municipalities = Municipality.objects.values("municipality_name").distinct()

    locations = Location.objects.all()

    context = {"announcement_number": announcement_number,"tab_number": tab_number,"unread_notifications": unread_notifications, "announcements": announcements, "municipalities": municipalities, "locations": locations}

    return render(request, "curator/control/announcement/announcement.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlAnnouncementRead(request, id):

    tab_number = 5

    announcement_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    announcement = get_object_or_404(Announcement, id = id)

    other_announcements = Announcement.objects.exclude(id = id)

    announcements = Announcement.objects.all().order_by("-event_date")

    municipalities = Location.objects.values("municipality").distinct()

    context = {"announcement_number": announcement_number,"tab_number": tab_number, "unread_notifications": unread_notifications, "announcement": announcement, "municipalities": municipalities, "other_announcements": other_announcements, "announcements": announcements}

    return render(request, "curator/control/announcement/read.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlAnnouncementAdd(request):
    tab_number = 5

    announcement_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    locations = Location.objects.all().distinct("municipality")

    municipalities = Municipality.objects.values("municipality_name").distinct()

    errors = None

    field_labels = None
    
    location_error = None

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, user = request.user.user)

        if form.is_valid():
            municipality = request.POST.get("municipality")

            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality__municipality_name = municipality, barangay__barangay_name = barangay)

                announcement = form.save(commit = False)

                announcement.location = location

                announcement.save()

                return redirect("Curator Control Announcement")

            except Location.DoesNotExist:
                location_error = "The municipality and barangay is empty."

        errors = form.errors.as_json()

        field_labels = {field.name: field.label for field in form}

    else:
        form = AnnouncementForm()

    context = {"announcement_number": announcement_number,"tab_number": tab_number, "unread_notifications": unread_notifications, "form": form, "municipalities": municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "curator/control/announcement/add.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlAnnouncementUpdate(request, id):
     
    tab_number = 5

    announcement_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)
    
    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
   
    announcement = get_object_or_404(Announcement, id = id)

    municipalities = Municipality.objects.values("municipality_name").distinct()
    
    locations = Location.objects.all().distinct("municipality")

    errors = None

    field_labels = None
    
    location_error = None

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance = announcement)

        if form.is_valid():
            municipality = request.POST.get("municipality")

            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality__municipality_name = municipality, barangay__barangay_name = barangay)

                updated_announcement = form.save(commit = False)

                updated_announcement.location = location

                updated_announcement.save()

                return redirect("Curator Control Announcement Read", id = id)

            except Location.DoesNotExist:
                location_error = "The municipality and barangay is empty."

        errors = form.errors.as_json()

        field_labels = {field.name: field.label for field in form}

    else:
        form = AnnouncementForm(instance = announcement)

    context = {"announcement_number": announcement_number, "tab_number": tab_number, "unread_notifications": unread_notifications, "form": form, "announcement": announcement, "municipalities": municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "curator/control/announcement/update.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlAnnouncementDelete(request, id):
    announcement = get_object_or_404(Announcement, id = id)

    if request.method == "DELETE":
        announcement.delete()

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})


def CuratorControlActivitySerialize(activities):
    activities_list = []

    for activity in activities:
        activities_list.append({"id": activity.id, "title": activity.title, "activity_date": activity.activity_date, "municipality": activity.location.municipality.municipality_name, "barangay": activity.location.barangay.barangay_name, "details": activity.details, "hosting_agency": activity.hosting_agency, "caught_amount": activity.caught_amount, "volunteer_amount": activity.volunteer_amount, "status": str(activity.statustype)})
    
    return json.dumps(activities_list, cls = DjangoJSONEncoder)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlActivity(request):
    tab_number =  4

    activity_number = 1

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    locations = Location.objects.all()

    activities = Activity.objects.all().order_by("-activity_date")

    municipalities = Municipality.objects.values("municipality_name").distinct()
    
    activities_json = CuratorControlActivitySerialize(activities)

    hosting_agencies = activities.values("hosting_agency").distinct()

    context = {"activity_number": activity_number, "tab_number": tab_number,  "unread_notifications": unread_notifications, "activities": activities, "municipalities": municipalities, "activities_json": activities_json, "locations": locations, "hosting_agencies": hosting_agencies}
    
    return render(request, "curator/control/activity/activity.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlActivityRead(request, id):
    tab_number =  4

    activity_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    activity = get_object_or_404(Activity, id = id)

    other_activities = Activity.objects.exclude(id = id)[:5]

    last_activity = (Activity.objects.filter(location = activity.location).exclude(id = id).order_by("-activity_date").first())

    context = {"activity_number": activity_number, "tab_number": tab_number, "unread_notifications": unread_notifications, "activity": activity, "other_activities": other_activities, "last_activity": last_activity}

    return render(request, "curator/control/activity/read.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlActivityAdd(request):
    tab_number =  4

    activity_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    municipalities = Municipality.objects.values('municipality_name').distinct()

    locations = Location.objects.all().distinct("municipality")

    errors = None

    field_labels = None

    location_error = None

    if request.method == "POST":

        form = ActivityForm(request.POST, request.FILES)

        if form.is_valid():

            municipality = request.POST.get("municipality")

            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality__municipality_name = municipality, barangay__barangay_name = barangay)

                activity = form.save(commit = False)
                
                activity.location = location

                activity.save()

                return redirect("Curator Control Activity")
            
            except Location.DoesNotExist:

                location_error = "The municipality and barangay is empty."

        errors = form.errors.as_json()

        field_labels = {field.name: field.label for field in form}

    else:
        form = ActivityForm()

    context = {"activity_number":activity_number, "tab_number": tab_number, "unread_notifications": unread_notifications, "form": form, 'municipalities': municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "curator/control/activity/add.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlActivityUpdate(request, id):
    tab_number =  4

    activity_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    activity = get_object_or_404(Activity, id = id)

    locations = Location.objects.all().distinct("municipality")

    municipalities = Municipality.objects.values("municipality_name").distinct()

    errors = None

    field_labels = None
    
    location_error = None
    
    if request.method == "POST":
        form = ActivityForm(request.POST, request.FILES, instance = activity)

        if form.is_valid():
            municipality = request.POST.get("municipality")

            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality__municipality_name = municipality, barangay__barangay_name = barangay)

                activity.location = location

                activity.creation_date = datetime.datetime.now()

                form.save()

                return redirect("Curator Control Activity")

            except Location.DoesNotExist:
                location_error = "The municipality and barangay is empty."

        errors = form.errors.as_json()

        field_labels = {field.name: field.label for field in form}

    else:
        form = ActivityForm(instance = activity)

    context = {"activity_number": activity_number, "tab_number": tab_number, "unread_notifications": unread_notifications, "form": form, "update": True, "activity": activity, "municipalities": municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "curator/control/activity/update.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlActivityDelete(request, id):
    activity = get_object_or_404(Activity, id = id)

    activity.delete()

    return JsonResponse({"success": True})


def CuratorControlStatusSerialize(statuses):
    statuses_list = []

    for status in statuses:
        statuses_list.append({"id": status.id, "statustype": str(status.statustype), "location": status.location.barangay + ", " + status.location.municipality, "caught_overall": status.caught_overall, "volunteer_overall": status.volunteer_overall, "onset_date": status.onset_date})
    
    return json.dumps(statuses_list, cls = DjangoJSONEncoder)


def CuratorControlStatusFetch(status_counts):
    features = []

    locations = {loc.id: loc for loc in Location.objects.all()} 

    status_types = {status.id: status.statustype for status in StatusType.objects.all()}

    for status in status_counts:
        location_id = status.get("location")

        count = status.get("count", 0)

        statustype_id = status.get("statustype")  

        location = locations.get(location_id)

        if not location:
            continue

        try:
            coordinates = json.loads(location.perimeters) 

            if not coordinates:
                continue

        except (json.JSONDecodeError, TypeError):
            continue

        statustype = status_types.get(statustype_id, "Unknown")

        features.append({"type": "Feature", "geometry": {"type": "Polygon", "coordinates": coordinates}, "properties": {"statustype": statustype, "count": count}})

    return {"type": "FeatureCollection", "features": features}


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlStatus(request):
    tab_number = 3

    location_number = 1

    notification_life = timezone.now() - timedelta(days = 30)

    municipality_filter = request.GET.get("municipality", "")

    status_filter = request.GET.get("status", "")

    status_queryset = Status.objects.all()

    if municipality_filter:
        status_queryset = status_queryset.filter(location__municipality__municipality_name = municipality_filter)
    
    if status_filter:
        status_queryset = status_queryset.filter(statustype__statustype = status_filter)

    status_counts = status_queryset.values("location", "statustype").annotate(count = Count("id"))

    geojson_data = CuratorControlStatusFetch(status_counts)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    latest_status_per_municipality = Status.objects.values("location__municipality").annotate(latest_date = Max("onset_date"))
   
    latest_statuses = []

    for entry in latest_status_per_municipality:
        status = Status.objects.filter(location__municipality = entry["location__municipality"]).order_by("-onset_date").first()
        
        if status:
            latest_statuses.append(status)

    if municipality_filter:
        latest_statuses = [status for status in latest_statuses if status.location.municipality.municipality_name == municipality_filter]
    
    if status_filter:
        latest_statuses = [status for status in latest_statuses if status.statustype.statustype == status_filter]

    paginator = Paginator(latest_statuses, 10)

    page_number = request.GET.get("page")

    paginated_statuses = paginator.get_page(page_number)

    municipalities = Location.objects.values_list("municipality__municipality_name", flat = True).distinct()

    statuses = Status.objects.values_list("statustype__statustype", flat = True).distinct()

    current_statuses = Status.objects.values("location__municipality__id", "location__municipality__municipality_name", "location__barangay__id", "location__barangay__barangay_name", "statustype__id", "onset_date").annotate(latest_date = Max("onset_date"))

    if municipality_filter:
        latest_statuses = [status for status in latest_statuses if status.location.municipality.municipality_name == municipality_filter]

        current_statuses = [status for status in current_statuses if status["location__municipality__municipality_name"] == municipality_filter]
    
    if status_filter:
        latest_statuses = [status for status in latest_statuses if status.statustype.statustype == status_filter]

        current_statuses = [status for status in current_statuses if status["statustype__statustype"] == status_filter]

    status_types = list(StatusType.objects.all().values("id", "statustype"))

    chart_data = {}

    for status in current_statuses:
        municipality_name = status["location__municipality__municipality_name"]

        barangay_name = status["location__barangay__barangay_name"]

        statustype_id = status["statustype__id"]

        date = status["latest_date"].strftime("%Y-%m-%d")

        if municipality_name not in chart_data:
            chart_data[municipality_name] = {}

        if statustype_id not in chart_data[municipality_name]:
            chart_data[municipality_name][statustype_id] = []

        existing_entry = next((item for item in chart_data[municipality_name][statustype_id] if item["barangay_name"] == barangay_name and item['date'] == date), None)
        
        if existing_entry:
            existing_entry["count"] += 1

        else:
            chart_data[municipality_name][statustype_id].append({"barangay_name": barangay_name, "date": date, "count": 1})

    context = {"geojson_data": json.dumps(geojson_data), "chart_data": json.dumps(chart_data), "status_types": json.dumps(status_types), "location_number": location_number, "tab_number": tab_number, "unread_notifications": unread_notifications, "locations": Location.objects.all(), "years": Status.objects.dates("onset_date", "year", order = "DESC"), "paginated_statuses": paginated_statuses, "municipalities": municipalities, "statuses": statuses,}

    return render(request, "curator/control/status/status.html", context)



@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlStatusMunicipalityRead(request, municipality_name):
    tab_number = 3

    location_number = 2 

    locations = Location.objects.filter(municipality__municipality_name = municipality_name)

    barangay_filter = request.GET.get("barangay", "")

    status_filter = request.GET.get("status", "")

    status_queryset = Status.objects.all()

    status_queryset = status_queryset.filter(location__municipality__municipality_name = municipality_name)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    if barangay_filter:
        status_queryset = status_queryset.filter(location__barangay__barangay_name = barangay_filter)
    
    if status_filter:
        status_queryset = status_queryset.filter(statustype__statustype = status_filter)

    status_counts = status_queryset.values("location", "statustype").annotate(count = Count("id"))
    
    geojson_data = CuratorControlStatusFetch(status_counts)

    latest_statuses = []

    for location in locations:
        latest_status = Status.objects.filter(location = location).order_by("-onset_date").first()

        if latest_status:
            latest_statuses.append(latest_status)

    barangays = Location.objects.filter(municipality__municipality_name = municipality_name).values_list("barangay__barangay_name", flat = True).distinct()
    
    statuses = Status.objects.values_list("statustype__statustype", flat = True).distinct()

    status_types = list(StatusType.objects.all().values("id", "statustype"))

    current_statuses = Status.objects.filter(location__barangay__municipality__municipality_name = municipality_name).values("location__barangay__id", "location__barangay__barangay_name", "statustype__id", "onset_date").annotate(latest_date = Max("onset_date"))

    if barangay_filter:
        latest_statuses = [status for status in latest_statuses if status.location.barangay.barangay_name == barangay_filter]
        
        current_statuses = [
            status for status in current_statuses 

            if status["location__barangay__barangay_name"] == barangay_filter
        ]

    if status_filter:
        latest_statuses = [status for status in latest_statuses if status.statustype.statustype == status_filter]

        current_statuses = [
            status for status in current_statuses 

            if status["statustype__statustype"] == status_filter
        ]

    chart_data = {}

    for status in current_statuses:
        barangay_id = status["location__barangay__id"]

        barangay_name = status["location__barangay__barangay_name"]

        statustype_id = status["statustype__id"]

        date = status["latest_date"].strftime("%Y-%m-%d")

        if barangay_name not in chart_data:
            chart_data[barangay_name] = {}

        chart_data[barangay_name][statustype_id] = {"count": chart_data[barangay_name].get(statustype_id, {"count": 0})["count"] + 1, "date": date}

    context = {"unread_notifications": unread_notifications, "geojson_data": json.dumps(geojson_data), "chart_data": json.dumps(chart_data), "status_types": json.dumps(status_types), "barangays": barangays, "statuses": statuses, "location_number": location_number, "tab_number": tab_number, "municipality_name": municipality_name, "latest_statuses": latest_statuses}

    return render(request, "curator/control/status/municipality.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlStatusBarangayRead(request, barangay_name):
    tab_number = 3

    location_number = 3

    status_filter = request.GET.get("status", "")

    locations = Location.objects.filter(barangay__barangay_name = barangay_name)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    if locations.exists():
        municipality_name = locations.first().municipality.municipality_name

    else:
        municipality_name = None

    all_statuses = Status.objects.filter(location__in = locations).order_by("-onset_date")

    status_filter = request.GET.get("status", "")

    if status_filter:
        all_statuses = [status for status in all_statuses if status.statustype.statustype == status_filter]
    
    statuses = Status.objects.values_list("statustype__statustype", flat = True).distinct()

    status_types = list(StatusType.objects.all().values("id", "statustype"))

    status_queryset = Status.objects.all()

    status_queryset = status_queryset.filter(location__municipality__municipality_name = municipality_name)

    status_queryset = status_queryset.filter(location__barangay__barangay_name = barangay_name)
    
    if status_filter:
        status_queryset = status_queryset.filter(statustype__statustype = status_filter)

    status_counts = status_queryset.values("location", "statustype").annotate(count = Count("id"))
    
    geojson_data = CuratorControlStatusFetch(status_counts)

    locations_query = Location.objects.all()

    locations_query = locations_query.filter(municipality__municipality_name = municipality_name)

    locations_query = locations_query.filter(barangay__barangay_name = barangay_name)

    data = []

    total_caught_overall = 0

    for location in locations:
        activities_query = Activity.objects.filter(location = location).order_by("activity_date")

        activity_dates = []

        caught_overalls = []
        
        titles = []
        
        status_types = []
        
        volunteer_amounts = []
        
        caught_overall_sum = 0

        for activity in activities_query:
            if activity.statustype:
                activity_dates.append(activity.activity_date.strftime("%Y-%m-%d"))

                caught_overalls.append(activity.caught_amount)
                
                titles.append(activity.title)
                
                status_types.append(str(activity.statustype))
                
                volunteer_amounts.append(activity.volunteer_amount)
                
                caught_overall_sum += activity.caught_amount

        total_caught_overall += caught_overall_sum

        if activity_dates:
            min_date = datetime.datetime.strptime(activity_dates[0], "%Y-%m-%d")

            max_date = datetime.datetime.strptime(activity_dates[-1], "%Y-%m-%d")
            
            current_date = min_date
            
            date_set = set(activity_dates)

            while current_date <= max_date:
                date_string = current_date.strftime("%Y-%m-%d")

                if date_string not in date_set:
                    activity_dates.append(date_string)
                
                    caught_overalls.append(None)
                
                    titles.append("N/A")
                
                    status_types.append("N/A")
                
                    volunteer_amounts.append(None)
                
                current_date += timedelta(days = 1)

            sorted_data = sorted(zip(activity_dates, caught_overalls, titles, status_types, volunteer_amounts))

            activity_dates, caught_overalls, titles, status_types, volunteer_amounts = zip(*sorted_data)

            for item in range(len(activity_dates)):
                data.append({"location": f"{location.barangay.barangay_name}, {location.municipality.municipality_name}", "municipality": location.municipality.municipality_name, "activity_date": activity_dates[item], "caught_amount": caught_overalls[item], "title": titles[item], "status_type": status_types[item], "volunteer_amount": volunteer_amounts[item]})


    context = {"unread_notifications": unread_notifications, "geojson_data": json.dumps(geojson_data), "chart_data": json.dumps(data), 'status_types': json.dumps(status_types), "municipality_name":municipality_name,"statuses":statuses,"location_number": location_number, "tab_number": tab_number, "barangay_name": barangay_name, "all_statuses": all_statuses}

    return render(request, "curator/control/status/barangay.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlStatusAdd(request):
    notification_life = timezone.now() - timedelta(days = 30) 

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    if request.method == "POST":
        form = StatusForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("Curator Control Status")
    else:
        form = StatusForm()

    context = {"unread_notifications": unread_notifications, "form": form}

    return render(request, "curator/control/status/add.html", context) 


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlDeleteStatus(request, id):
    if request.method == "POST":
        status = get_object_or_404(Status, id = id)

        status.delete()

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False}, status = 400)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlBarangayRead(request):
    municipality = request.GET.get("municipality")

    barangays = Barangay.objects.filter(municipality__municipality_name = municipality).values_list("barangay_name", flat = True).distinct()
    
    return JsonResponse(list(barangays), safe = False)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlReport(request):
    username = request.user.username

    notification_life = timezone.now() - timedelta(days = 30)
    
    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    selected_status = request.GET.get("status")

    selected_municipality = request.GET.get("municipalityFilter")

    selected_barangay = request.GET.get("barangayFilter")
  
    if from_date:
        from_date = parse_date(from_date)

    if to_date:
        to_date = parse_date(to_date)

    status_options = StatusType.objects.all()

    location_options = Location.objects.all()

    status_query = Q()

    if from_date:
        status_query &= Q(onset_date__gte = from_date)

    if to_date:
        status_query &= Q(onset_date__lte = to_date)

    if selected_status:
        status_query &= Q(statustype = selected_status)

    if selected_municipality:
        status_query &= Q(location__municipality__municipality_name = selected_municipality)

    if selected_barangay:
        status_query &= Q(location__barangay__barangay_name = selected_barangay)

    statuses = Status.objects.filter(status_query).order_by("-onset_date")

    municipalities = Municipality.objects.values("municipality_name").distinct()

    barangays = Barangay.objects.filter(municipality__municipality_name = selected_municipality).values("barangay_name").distinct() if selected_municipality else []

    data = {}
    
    results = statuses

    for location in location_options:
        location_str = f"{location.barangay}, {location.municipality}"
        
        location_statuses = statuses.filter(location=location).order_by("onset_date")
        
        data[location_str] = {"onset_dates": [status.onset_date.strftime("%Y-%m-%d") for status in location_statuses], "caught_overalls": [status.caught_overall for status in location_statuses]}

    context = {"username": username, "unread_notifications": unread_notifications, "chart_data": json.dumps(data), "status_options": status_options, "location_options": location_options, "results": results, "from_date": from_date, "to_date": to_date, "selected_status": selected_status, "selected_municipality": selected_municipality, "selected_barangay": selected_barangay, "municipalities": municipalities, "barangays": barangays}

    return render(request, "curator/control/report/report.html", context)