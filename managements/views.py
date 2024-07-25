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
from authentications.views import ContributorCheck, OfficerCheck
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

    announcements = Announcement.objects.all().order_by("-release_date")

    if municipality:
        announcements = announcements.filter(location__municipality__municipality_name = municipality)

    if barangay:
        announcements = announcements.filter(location__barangay__barangay_name = barangay)

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


def PublicServiceIntervention(request):
    username = "public/everyone"

    locations = Location.objects.all()

    municipalities = Municipality.objects.values("municipality_name").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    interventions = Intervention.objects.all().order_by("-event_date")

    if municipality:
        interventions = interventions.filter(location__municipality__municipality_name = municipality)

    if barangay:
        interventions = interventions.filter(location__barangay__barangay_name = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        interventions = interventions.filter(event_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        interventions = interventions.filter(event_date__lte = to_date)

    context = {"username": username, "locations": locations, "municipalities": municipalities, "interventions": interventions}

    return render(request, "public/service/intervention/intervention.html", context)


def PublicServiceInterventionRead(request, id):
    username = "public/everyone"

    scheme = request.scheme

    host = request.META["HTTP_HOST"]
    
    intervention = Intervention.objects.get(id = id)

    context = {"username": username, "scheme": scheme, "host": host, "intervention": intervention}

    return render(request, "public/service/intervention/read.html", context)


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

    announcements = Announcement.objects.all().order_by("-release_date")

    if municipality:
        announcements = announcements.filter(location__municipality__municipality_name = municipality)

    if barangay:
        announcements = announcements.filter(location__barangay__barangay_name = barangay)

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
def ContributorServiceIntervention(request):
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

    interventions = Intervention.objects.all().order_by("-event_date")

    if municipality:
        interventions = interventions.filter(location__municipality__municipality_name = municipality)

    if barangay:
        interventions = interventions.filter(location__barangay__barangay_name = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        interventions = interventions.filter(event_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        interventions = interventions.filter(event_date__lte = to_date)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "locations": locations, "municipalities": municipalities, "interventions": interventions}

    return render(request, "contributor/service/intervention/intervention.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceInterventionRead(request, id):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    intervention = Intervention.objects.get(id = id)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "scheme": scheme, "host": host, "intervention": intervention}

    return render(request, "contributor/service/intervention/read.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncement(request):
    tab_number = 5

    ann_number = 1

    notification_life = timezone.now() - timedelta(days = 30) 

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
   
    announcements = Announcement.objects.all().order_by("-release_date")

    municipalities = Municipality.objects.values("municipality_name").distinct()

    locations = Location.objects.all()

    context = {"ann_number": ann_number,"tab_number": tab_number,"unread_notifications": unread_notifications, "announcements": announcements, "municipalities": municipalities, "locations": locations}

    return render(request, "officer/control/announcement/announcement.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncementRead(request, id):

    tab_number = 5

    ann_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    announcement = get_object_or_404(Announcement, id = id)

    other_announcements = Announcement.objects.exclude(id = id)

    announcements = Announcement.objects.all().order_by("-release_date")

    municipalities = Location.objects.values("municipality").distinct()

    context = {"ann_number": ann_number,"tab_number": tab_number, "unread_notifications": unread_notifications, "announcement": announcement, "municipalities": municipalities, "other_announcements": other_announcements, "announcements": announcements}

    return render(request, "officer/control/announcement/read.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncementAdd(request):
    tab_number = 5

    ann_number = 2

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

                return redirect("Officer Control Announcement")

            except Location.DoesNotExist:
                location_error = "The municipality and barangay is empty."

        errors = form.errors.as_json()

        field_labels = {field.name: field.label for field in form}

    else:
        form = AnnouncementForm()

    context = {"ann_number": ann_number,"tab_number": tab_number, "unread_notifications": unread_notifications, "form": form, "municipalities": municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "officer/control/announcement/add.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncementUpdate(request, id):
     
    tab_number = 5

    ann_number = 2

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

                return redirect("Officer Control Announcement Read", id = id)

            except Location.DoesNotExist:
                location_error = "The municipality and barangay is empty."

        errors = form.errors.as_json()

        field_labels = {field.name: field.label for field in form}

    else:
        form = AnnouncementForm(instance = announcement)

    context = {"ann_number": ann_number,"tab_number": tab_number, "unread_notifications": unread_notifications, "form": form, "announcement": announcement, "municipalities": municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "officer/control/announcement/update.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncementDelete(request, id):
    announcement = get_object_or_404(Announcement, id = id)

    if request.method == "DELETE":
        announcement.delete()

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})


def OfficerControlInterventionSerialize(interventions):
    interventions_list = []

    for intervention in interventions:
        interventions_list.append({"id": intervention.id, "title": intervention.title, "event_date": intervention.event_date, "municipality": intervention.location.municipality.municipality_name, "barangay": intervention.location.barangay.barangay_name, "details": intervention.details, "hosting_agency": intervention.hosting_agency, "caught_amount": intervention.caught_amount, "volunteer_amount": intervention.volunteer_amount, "status": str(intervention.statustype)})
    
    return json.dumps(interventions_list, cls = DjangoJSONEncoder)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlIntervention(request):
    tab_number =  4

    int_number = 1

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    locations = Location.objects.all()

    interventions = Intervention.objects.all().order_by("-event_date")

    municipalities = Municipality.objects.values("municipality_name").distinct()
    
    interventions_json = OfficerControlInterventionSerialize(interventions)

    hosting_agencies = interventions.values("hosting_agency").distinct()

    context = {"int_number": int_number, "tab_number": tab_number,  "unread_notifications": unread_notifications, "interventions": interventions, "municipalities": municipalities, "interventions_json": interventions_json, "locations": locations, "hosting_agencies": hosting_agencies}
    
    return render(request, "officer/control/intervention/intervention.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlInterventionRead(request, id):
    tab_number =  4

    int_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    intervention = get_object_or_404(Intervention, id = id)

    other_interventions = Intervention.objects.exclude(id = id)[:5]

    last_intervention = (Intervention.objects.filter(location = intervention.location).exclude(id = id).order_by("-event_date").first())

    context = {"int_number":int_number, "tab_number": tab_number, "unread_notifications": unread_notifications, "intervention": intervention, "other_interventions": other_interventions, "last_intervention": last_intervention }

    return render(request, "officer/control/intervention/read.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlInterventionAdd(request):
    tab_number =  4

    int_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    municipalities = Municipality.objects.values('municipality_name').distinct()

    locations = Location.objects.all().distinct("municipality")

    errors = None

    field_labels = None

    location_error = None

    if request.method == "POST":

        form = InterventionForm(request.POST, request.FILES)

        if form.is_valid():

            municipality = request.POST.get("municipality")

            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality__municipality_name = municipality, barangay__barangay_name = barangay)

                intervention = form.save(commit=False)
                
                intervention.location = location

                intervention.save()

                return redirect("Officer Control Intervention")
            
            except Location.DoesNotExist:

                location_error = "The municipality and barangay is empty."

        errors = form.errors.as_json()

        field_labels = {field.name: field.label for field in form}

    else:
        form = InterventionForm()

    context = {"int_number":int_number, "tab_number": tab_number, "unread_notifications": unread_notifications, "form": form, 'municipalities': municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "officer/control/intervention/add.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlInterventionUpdate(request, id):
    tab_number =  4

    int_number = 2

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    intervention = get_object_or_404(Intervention, id = id)

    locations = Location.objects.all().distinct("municipality")

    municipalities = Municipality.objects.values("municipality_name").distinct()

    errors = None

    field_labels = None
    
    location_error = None
    
    if request.method == "POST":
        form = InterventionForm(request.POST, request.FILES, instance = intervention)

        if form.is_valid():
            municipality = request.POST.get("municipality")

            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality__municipality_name = municipality, barangay__barangay_name = barangay)

                intervention.location = location

                intervention.creation_date = datetime.datetime.now()

                form.save()

                return redirect("Officer Control Intervention")

            except Location.DoesNotExist:
                location_error = "The municipality and barangay is empty."

        errors = form.errors.as_json()

        field_labels = {field.name: field.label for field in form}

    else:
        form = InterventionForm(instance = intervention)

    context = {"int_number":int_number, "tab_number": tab_number, "unread_notifications": unread_notifications, "form": form, "update": True, "intervention": intervention, "municipalities": municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "officer/control/intervention/update.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlInterventionDelete(request, id):
    intervention = get_object_or_404(Intervention, id = id)

    intervention.delete()

    return JsonResponse({"success": True})


def OfficerControlStatusSerialize(statuses):
    statuses_list = []

    for status in statuses:
        statuses_list.append({"id": status.id, "statustype": str(status.statustype), "location": status.location.barangay + ", " + status.location.municipality, "caught_overall": status.caught_overall, "volunteer_overall": status.volunteer_overall, "onset_date": status.onset_date})
    
    return json.dumps(statuses_list, cls = DjangoJSONEncoder)


def get_geojson_data(status_counts):
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


def OfficerControlStatus(request):
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

    geojson_data = get_geojson_data(status_counts)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user=user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    latest_status_per_municipality = Status.objects.values("location__municipality").annotate(latest_date = Max("onset_date"))
   
    latest_statuses = []

    for entry in latest_status_per_municipality:
        status = Status.objects.filter(location__municipality=entry["location__municipality"]).order_by("-onset_date").first()
        
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

    return render(request, "officer/control/status/status.html", context)



@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatusMunicipalityRead(request, municipality_name):
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
    
    geojson_data = get_geojson_data(status_counts)

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

    return render(request, "officer/control/status/municipality.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatusBarangayRead(request, barangay_name):
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
    
    geojson_data = get_geojson_data(status_counts)

    locations_query = Location.objects.all()

    locations_query = locations_query.filter(municipality__municipality_name = municipality_name)

    locations_query = locations_query.filter(barangay__barangay_name = barangay_name)

    data = []

    total_caught_overall = 0

    for location in locations:
        interventions_query = Intervention.objects.filter(location = location).order_by("event_date")
    

        event_dates = []

        caught_overalls = []
        
        titles = []
        
        status_types = []
        
        volunteer_amounts = []
        
        caught_overall_sum = 0

        for intervention in interventions_query:
            if intervention.statustype:
                event_dates.append(intervention.event_date.strftime("%Y-%m-%d"))

                caught_overalls.append(intervention.caught_amount)
                
                titles.append(intervention.title)
                
                status_types.append(str(intervention.statustype))
                
                volunteer_amounts.append(intervention.volunteer_amount)
                
                caught_overall_sum += intervention.caught_amount

        total_caught_overall += caught_overall_sum

        if event_dates:
            min_date = datetime.datetime.strptime(event_dates[0], "%Y-%m-%d")

            max_date = datetime.datetime.strptime(event_dates[-1], "%Y-%m-%d")
            
            current_date = min_date
            
            date_set = set(event_dates)

            while current_date <= max_date:
                date_string = current_date.strftime("%Y-%m-%d")

                if date_string not in date_set:
                    event_dates.append(date_string)
                
                    caught_overalls.append(None)
                
                    titles.append("N/A")
                
                    status_types.append("N/A")
                
                    volunteer_amounts.append(None)
                
                current_date += timedelta(days = 1)

            sorted_data = sorted(zip(event_dates, caught_overalls, titles, status_types, volunteer_amounts))

            event_dates, caught_overalls, titles, status_types, volunteer_amounts = zip(*sorted_data)

            for item in range(len(event_dates)):
                data.append({"location": f"{location.barangay.barangay_name}, {location.municipality.municipality_name}", "municipality": location.municipality.municipality_name, "event_date": event_dates[item], "caught_amount": caught_overalls[item], "title": titles[item], "status_type": status_types[item], "volunteer_amount": volunteer_amounts[item]})


    context = {"unread_notifications": unread_notifications, "geojson_data": json.dumps(geojson_data), "chart_data": json.dumps(data), 'status_types': json.dumps(status_types), "municipality_name":municipality_name,"statuses":statuses,"location_number": location_number, "tab_number": tab_number, "barangay_name": barangay_name, "all_statuses": all_statuses}

    return render(request, "officer/control/status/barangay.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatusAdd(request):
    notification_life = timezone.now() - timedelta(days = 30) 

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    if request.method == "POST":
        form = StatusForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("Officer Control Status")
    else:
        form = StatusForm()

    context = {"unread_notifications": unread_notifications, "form": form}

    return render(request, "officer/control/status/add.html", context) 


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlDeleteStatus(request, id):
    if request.method == "POST":
        status = get_object_or_404(Status, id = id)

        status.delete()

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False}, status = 400)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlBarangayRead(request):
    municipality = request.GET.get("municipality")

    barangays = Barangay.objects.filter(municipality__municipality_name = municipality).values_list("barangay_name", flat = True).distinct()
    
    return JsonResponse(list(barangays), safe = False)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlReport(request):
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

    return render(request, "officer/control/report/report.html", context)