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


def PublicServiceIntervention(request):
    username = "public/everyone"

    locations = Location.objects.all()

    municipalities = Location.objects.values("municipality").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    interventions = Intervention.objects.all().order_by("-event_date")

    if municipality:
        interventions = interventions.filter(location__municipality = municipality)

    if barangay:
        interventions = interventions.filter(location__barangay = barangay)

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

    municipalities = Location.objects.values("municipality").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    interventions = Intervention.objects.all().order_by("-event_date")

    if municipality:
        interventions = interventions.filter(location__municipality = municipality)

    if barangay:
        interventions = interventions.filter(location__barangay = barangay)

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
    notification_life = timezone.now() - timedelta(days = 30) 

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
   
    announcements = Announcement.objects.all().order_by("-release_date")

    municipalities = Municipality.objects.values("municipality_name").distinct()

    locations = Location.objects.all()

    context = {"unread_notifications": unread_notifications, "announcements": announcements, "municipalities": municipalities, "locations": locations}

    return render(request, "officer/control/announcement/announcement.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncementRead(request, id):
    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    announcement = get_object_or_404(Announcement, id = id)

    other_announcements = Announcement.objects.exclude(id = id)

    announcements = Announcement.objects.all().order_by("-release_date")

    municipalities = Location.objects.values("municipality").distinct()

    context = {"unread_notifications": unread_notifications, "announcement": announcement, "municipalities": municipalities, "other_announcements": other_announcements, "announcements": announcements}

    return render(request, "officer/control/announcement/read.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncementAdd(request):
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

    context = {"unread_notifications": unread_notifications, "form": form, "municipalities": municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "officer/control/announcement/add.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlAnnouncementUpdate(request, id):
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

    context = {"unread_notifications": unread_notifications, "form": form, "announcement": announcement, "municipalities": municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

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

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    locations = Location.objects.all()

    interventions = Intervention.objects.all().order_by("-event_date")

    municipalities = Municipality.objects.values("municipality_name").distinct()
    
    interventions_json = OfficerControlInterventionSerialize(interventions)

    hosting_agencies = interventions.values("hosting_agency").distinct()

    context = {"unread_notifications": unread_notifications, "interventions": interventions, "municipalities": municipalities, "interventions_json": interventions_json, "locations": locations, "hosting_agencies": hosting_agencies}
    
    return render(request, "officer/control/intervention/intervention.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlInterventionRead(request, id):
    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    intervention = get_object_or_404(Intervention, id = id)

    other_interventions = Intervention.objects.exclude(id = id)[:5]

    last_intervention = (Intervention.objects.filter(location = intervention.location).exclude(id = id).order_by("-event_date").first())

    context = {"unread_notifications": unread_notifications, "intervention": intervention, "other_interventions": other_interventions, "last_intervention": last_intervention }

    return render(request, "officer/control/intervention/read.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlInterventionAdd(request):
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

    context = {"unread_notifications": unread_notifications, "form": form, 'municipalities': municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "officer/control/intervention/add.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlInterventionUpdate(request, id):
    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    intervention = get_object_or_404(Intervention, id = id)

    locations = Location.objects.all().distinct("municipality")

    municipalities = Municipality.objects.values('municipality_name').distinct()

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

    context = {"unread_notifications": unread_notifications, "form": form, "update": True, "intervention": intervention, "municipalities": municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

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


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatus(request):
    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    latest_status_per_municipality = Status.objects.values("location__municipality").annotate(latest_date=Max("onset_date"))

    latest_statuses = []

    for entry in latest_status_per_municipality:
        status = Status.objects.filter(location__municipality=entry["location__municipality"]).order_by("-onset_date").first()

        if status:
            print(status)
            latest_statuses.append(status)

    paginator = Paginator(latest_statuses, 10)

    page_number = request.GET.get("page")

    paginated_statuses = paginator.get_page(page_number)

    context = {"unread_notifications": unread_notifications, "locations": Location.objects.all(), "years": Status.objects.dates("onset_date", "year", order = "DESC"), "paginated_statuses": paginated_statuses,}

    return render(request, "officer/control/status/status.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatusMunicipalityRead(request, municipality_name):
    locations = Location.objects.filter(municipality__municipality_name = municipality_name)

    latest_statuses = []

    for location in locations:
        latest_status = Status.objects.filter(location = location).order_by("-onset_date").first()

        if latest_status:
            latest_statuses.append(latest_status)

    context = {"municipality_name": municipality_name, "latest_statuses": latest_statuses}

    return render(request, "officer/control/status/municipality.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatusBarangayRead(request, barangay_name):
    locations = Location.objects.filter(barangay__barangay_name = barangay_name)
    
    all_statuses = Status.objects.filter(location__in = locations).order_by("-onset_date")

    context = {"barangay_name": barangay_name, "all_statuses": all_statuses}

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

    barangays = Barangay.objects.filter(municipality__municipality_name=selected_municipality).values("barangay_name").distinct() if selected_municipality else []

    print(barangays)

    data = {}
    
    results = statuses

    for location in location_options:
        location_str = f"{location.barangay}, {location.municipality}"
        
        location_statuses = statuses.filter(location=location).order_by("onset_date")
        
        data[location_str] = {"onset_dates": [status.onset_date.strftime("%Y-%m-%d") for status in location_statuses], "caught_overalls": [status.caught_overall for status in location_statuses]}

    context = {"username": username, "unread_notifications": unread_notifications, "chart_data": json.dumps(data), "status_options": status_options, "location_options": location_options, "results": results, "from_date": from_date, "to_date": to_date, "selected_status": selected_status, "selected_municipality": selected_municipality, "selected_barangay": selected_barangay, "municipalities": municipalities, "barangays": barangays}

    return render(request, "officer/control/report/report.html", context)