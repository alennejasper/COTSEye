from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.dateparse import parse_date
from authentications.views import ContributorCheck, OfficerCheck, AdministratorCheck
from collections import Counter
from authentications.models import User
from managements.models import *
from reports.models import Post
from .forms import InterventionForm, StatusForm
from .models import Intervention
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.dateformat import DateFormat

import datetime
import json


# Create your views here.
def PublicServiceIntervention(request):
    username = "public/everyone"

    locations = Location.objects.all()

    municipalities = Location.objects.values("municipality").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    interventions = Intervention.objects.all().order_by("-intervention_date")

    if municipality:
        interventions = interventions.filter(location__municipality = municipality)

    if barangay:
        interventions = interventions.filter(location__barangay = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        interventions = interventions.filter(intervention_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        interventions = interventions.filter(intervention_date__lte = to_date)

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
def ContributorServiceIntervention(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    locations = Location.objects.all()

    municipalities = Location.objects.values("municipality").distinct()

    municipality = request.GET.get("municipality")

    barangay = request.GET.get("barangay")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")

    interventions = Intervention.objects.all().order_by("-intervention_date")

    if municipality:
        interventions = interventions.filter(location__municipality = municipality)

    if barangay:
        interventions = interventions.filter(location__barangay = barangay)

    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')

        interventions = interventions.filter(intervention_date__gte = from_date)
    
    if to_date:
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        interventions = interventions.filter(intervention_date__lte = to_date)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "locations": locations, "municipalities": municipalities, "interventions": interventions}

    return render(request, "contributor/service/intervention/intervention.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceInterventionRead(request, id):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    intervention = Intervention.objects.get(id = id)

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "scheme": scheme, "host": host, "intervention": intervention}

    return render(request, "contributor/service/intervention/read.html", context)


def serialize_interventions(interventions):
    interventions_list = []

    for intervention in interventions:
        interventions_list.append({
            "id": intervention.id,
            "title": intervention.title,
            "intervention_date": intervention.intervention_date,
            "municipality": intervention.location.municipality,
            "barangay": intervention.location.barangay,
            "details": intervention.details,
            "hosting_agency": intervention.hosting_agency,
            "caught_amount": intervention.caught_amount,
            "volunteer_amount": intervention.volunteer_amount,
            "status": str(intervention.statustype)

        })
    
    return json.dumps(interventions_list, cls=DjangoJSONEncoder)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlIntervention(request):
    notification_life = timezone.now() - timedelta(days = 30) 

    unread_notifications = Post.objects.filter(read_status = False, creation_date__gte = notification_life).order_by("-creation_date")[:5]

    locations = Location.objects.all()

    interventions = Intervention.objects.all().order_by('-intervention_date')

    municipalities = Location.objects.values('municipality').distinct()
    
    interventions_json = serialize_interventions(interventions)

    hosting_agencies = interventions.values("hosting_agency").distinct()

    context = {"unread_notifications": unread_notifications, "interventions": interventions, 'municipalities': municipalities, "interventions_json": interventions_json, "locations": locations, "hosting_agencies": hosting_agencies}
    
    return render(request, "officer/control/intervention/intervention.html", context)

from django.utils import timezone
from datetime import timedelta

@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def OfficerControlInterventionAdd(request):
    notification_life = timezone.now() - timedelta(days=30)

    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by("-creation_date")[:5]

    municipalities = Location.objects.values('municipality').distinct()

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
                location = Location.objects.get(municipality=municipality, barangay=barangay)

                intervention = form.save(commit=False)
                
                intervention.location = location

                intervention.save()

                return redirect("Officer Control Intervention")
            
            except Location.DoesNotExist:

                location_error = "The selected location does not exist."

        errors = form.errors.as_json()
        field_labels = {field.name: field.label for field in form}
    else:

        form = InterventionForm()

    context = {"unread_notifications": unread_notifications, "form": form, 'municipalities': municipalities, "locations": locations, "errors": errors, "field_labels": field_labels, "location_error": location_error}

    return render(request, "officer/control/intervention/addintervention.html", context)


@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def OfficerControlInterventionUpdate(request, pk):
    notification_life = timezone.now() - timedelta(days=30)

    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by("-creation_date")[:5]

    intervention = get_object_or_404(Intervention, pk=pk)

    locations = Location.objects.all().distinct("municipality")
    municipalities = Location.objects.values('municipality').distinct()

    errors = None
    field_labels = None
    location_error = None
    if request.method == "POST":
        form = InterventionForm(request.POST, request.FILES, instance=intervention)

        if form.is_valid():
            municipality = request.POST.get("municipality")
            barangay = request.POST.get("barangay")

            try:
                location = Location.objects.get(municipality=municipality, barangay=barangay)

                intervention.location = location
                form.save()

                return redirect("Officer Control Intervention")

            except Location.DoesNotExist:
                
                location_error = "The selected location does not exist."

        errors = form.errors.as_json()
        field_labels = {field.name: field.label for field in form}

    else:
        form = InterventionForm(instance=intervention)

    context = {
        "unread_notifications": unread_notifications,
        "form": form,
        "update": True,
        "intervention": intervention,
        "municipalities": municipalities,
        "locations": locations,
        "errors": errors,
        "field_labels": field_labels,
        "location_error": location_error
    }

    return render(request, "officer/control/intervention/updateintervention.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlInterventionDelete(request, pk):
    intervention = get_object_or_404(Intervention, id = pk)

    intervention.delete()

    return JsonResponse({"success": True})


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlInterventionDetail(request, pk):
    notification_life = timezone.now() - timedelta(days = 30)

    unread_notifications = Post.objects.filter(read_status = False, creation_date__gte = notification_life).order_by("-creation_date")[:5]

    intervention = get_object_or_404(Intervention, id = pk)

    other_interventions = Intervention.objects.exclude(pk = pk)[:5]
    last_intervention = (Intervention.objects
                        .filter(location=intervention.location)
                        .exclude(pk=pk)
                        .order_by('-intervention_date')
                        .first())

    context = {"unread_notifications": unread_notifications, "intervention": intervention, "other_interventions": other_interventions, "last_intervention": last_intervention }

    return render(request, "officer/control/intervention/detailintervention.html", context)

def serialize_statuses(statuses):
    statuses_list = []

    for status in statuses:
        statuses_list.append({
            "id": status.id,
            "statustype": str(status.statustype),
            "location": status.location.barangay + ", " + status.location.municipality,
            "caught_overall": status.caught_overall,
            "volunteer_overall": status.volunteer_overall,  # Include volunteer_overall
            "onset_date": status.onset_date
        })
    
    return json.dumps(statuses_list, cls=DjangoJSONEncoder)

@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def OfficerControlStatus(request):
    notification_life = timezone.now() - timedelta(days=30)
    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by("-creation_date")[:5]

    statuses = Status.objects.all().order_by('-onset_date')
    locations = Location.objects.all()

    # Filtering based on year
    year_filter = request.GET.get('year')
    if year_filter:
        statuses = statuses.filter(onset_date__year=year_filter)

    # Sorting
    sort_by = request.GET.get('sort', 'onset_date')
    sort_order = request.GET.get('order', 'desc')
    if sort_by in ['statustype', 'caught_overall', 'volunteer_overall', 'onset_date']:
        if sort_order == 'asc':
            statuses = statuses.order_by(sort_by)
        else:
            statuses = statuses.order_by(f'-{sort_by}')

    # Organize statuses by municipality and barangay
    municipalities = {}
    for status in statuses:
        municipality = status.location.municipality
        barangay = status.location.barangay

        if municipality not in municipalities:
            municipalities[municipality] = {
                'latest_status': None,
                'barangays': {}
            }

        if barangay not in municipalities[municipality]['barangays']:
            municipalities[municipality]['barangays'][barangay] = {
                'latest_status': None,
                'statuses': []
            }

        municipalities[municipality]['barangays'][barangay]['statuses'].append(status)

    # Get latest status for each barangay and municipality and set totals based on latest status
    for municipality, data in municipalities.items():
        for barangay, barangay_data in data['barangays'].items():
            if barangay_data['statuses']:
                latest_status = max(barangay_data['statuses'], key=lambda status: status.onset_date)
                latest_status.onset_date = DateFormat(latest_status.onset_date).format('m/d/Y')
                barangay_data['latest_status'] = latest_status
                barangay_data['total_caught'] = latest_status.caught_overall or 0
                barangay_data['total_volunteers'] = latest_status.volunteer_overall or 0
            else:
                barangay_data['total_caught'] = 0
                barangay_data['total_volunteers'] = 0
        
        data['total_caught'] = sum(barangay_data['total_caught'] for barangay_data in data['barangays'].values())
        data['total_volunteers'] = sum(barangay_data['total_volunteers'] for barangay_data in data['barangays'].values())
        if data['barangays']:
            data['latest_status'] = max(
                (barangay_data['latest_status'] for barangay_data in data['barangays'].values() if barangay_data['latest_status']),
                key=lambda status: status.onset_date
            )

    # Pagination
    paginator = Paginator(statuses, 10)  # Show 10 statuses per page
    page_number = request.GET.get('page')
    paginated_statuses = paginator.get_page(page_number)

    statuses_json = serialize_statuses(statuses)

    context = {
        "unread_notifications": unread_notifications,
        "municipalities": municipalities,
        "statuses_json": statuses_json,
        "locations": locations,
        "year_filter": year_filter,
        "years": Status.objects.dates('onset_date', 'year', order='DESC'),
        "paginated_statuses": paginated_statuses,
        "sort_by": sort_by,
        "sort_order": sort_order,
    }

    return render(request, "officer/control/status/status.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlDeleteStatus(request, status_id):
    if request.method == "POST":
        status = get_object_or_404(Status, id = status_id)

        status.delete()

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False}, status = 400)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatusAdd(request):
    notification_life = timezone.now() - timedelta(days = 30) 

    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by("-creation_date")[:5]

    if request.method == "POST":
        form = StatusForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("Officer Control Status")
    else:
        form = StatusForm()

    context = {"unread_notifications": unread_notifications, "form": form}

    return render(request, "officer/control/status/addstatus.html", context) 


@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def OfficerControlReport(request):
    username = request.user.username

    notification_life = timezone.now() - timedelta(days=30)
    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by('-creation_date')[:5]

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
        status_query &= Q(onset_date__gte=from_date)
    if to_date:
        status_query &= Q(onset_date__lte=to_date)
    if selected_status:
        status_query &= Q(statustype=selected_status)
    if selected_municipality:
        status_query &= Q(location__municipality=selected_municipality)
    if selected_barangay:
        status_query &= Q(location__barangay=selected_barangay)

    statuses = Status.objects.filter(status_query).order_by('-onset_date')
    municipalities = Location.objects.values("municipality").distinct()
    barangays = Location.objects.filter(municipality=selected_municipality).values("barangay").distinct() if selected_municipality else []

    data = {}
    results = statuses

    for location in location_options:
        location_str = f"{location.barangay}, {location.municipality}"
        location_statuses = statuses.filter(location=location).order_by("onset_date")
        data[location_str] = {
            "onset_dates": [status.onset_date.strftime("%Y-%m-%d") for status in location_statuses],
            "caught_overalls": [status.caught_overall for status in location_statuses]
        }

    context = {
        "username": username,
        "unread_notifications": unread_notifications,
        "chart_data": json.dumps(data),
        "status_options": status_options,
        "location_options": location_options,
        "results": results,
        "from_date": from_date,
        "to_date": to_date,
        "selected_status": selected_status,
        "selected_municipality": selected_municipality,
        "selected_barangay": selected_barangay,
        "municipalities": municipalities,
        "barangays": barangays,
    }

    return render(request, "officer/control/report/report.html", context)


@login_required(login_url = "admin:Administrator Control Login")
@user_passes_test(AdministratorCheck, login_url = "admin:Administrator Control Login")
def AdministratorControlStatisticsIntervention(request):
    username = request.user.username

    options = Intervention.objects.all()

    records = Intervention.objects.all()

    results = None

    try:
        interventions_count = records.count()

        interventions_label = "Interventions" + " Count"
    
    except:
        interventions_count = ""

        interventions_label = ""
    
    try:
        locations_count = records.count()

        locations_label = "Locations" + " Count"
    
    except:
        locations_count = ""

        locations_label = ""
    
    try:
        caughtamount_distribution = [str(caught_amount.caught_amount) for caught_amount in records]

        caughtamount_tally = Counter(caughtamount_distribution)

        caughtamount_frequency = caughtamount_tally.most_common(1)[0][0]

    except:
        caughtamount_frequency = ""
    
    try:
        caughtamount_firstfrequency = caughtamount_tally.most_common(1)[0][1]

        caughtamount_firstlabel = caughtamount_tally.most_common(1)[0][0] + " / Sqauare Meter Mode"

    except:
        caughtamount_firstfrequency = ""
    
        caughtamount_firstlabel = ""
    
    try:
        caughtamount_secondfrequency = caughtamount_tally.most_common(2)[1][1]

        caughtamount_secondlabel = caughtamount_tally.most_common(2)[1][0] + " / Sqauare Meter Mode"
    
    except:
        caughtamount_secondfrequency = ""
    
        caughtamount_secondlabel = ""
    
    try:
        caughtamount_thirdfrequency = caughtamount_tally.most_common(3)[2][1] 

        caughtamount_thirdlabel = caughtamount_tally.most_common(3)[2][0] + " Mode"
    
    except:
        caughtamount_thirdfrequency = ""
    
        caughtamount_thirdlabel = ""

    try:
        hostingagency_distribution = [str(hosting_agency.hosting_agency) for hosting_agency in records]

        hostingagency_tally = Counter(hostingagency_distribution)

        hostingagency_frequency = hostingagency_tally.most_common(1)[0][0]

    except:
        hostingagency_frequency = ""
    
    try:
        hostingagency_firstfrequency = hostingagency_tally.most_common(1)[0][1]

        hostingagency_firstlabel = hostingagency_tally.most_common(1)[0][0] + " Mode"

    except:
        hostingagency_firstfrequency = ""
    
        hostingagency_firstlabel = ""
    
    try:
        hostingagency_secondfrequency = hostingagency_tally.most_common(2)[1][1]

        hostingagency_secondlabel = hostingagency_tally.most_common(2)[1][0] + " Mode"
    
    except:
        hostingagency_secondfrequency = ""
    
        hostingagency_secondlabel = ""
    
    try:
        hostingagency_thirdfrequency = hostingagency_tally.most_common(3)[2][1] 

        hostingagency_thirdlabel = hostingagency_tally.most_common(3)[2][0] + " Mode"
    
    except:
        hostingagency_thirdfrequency = ""
    
        hostingagency_thirdlabel = ""
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        location = request.GET.get("location")

        hosting_agency = request.GET.get("hosting_agency")

        if from_date and to_date:
            results = Intervention.objects.filter(intervention_date__range = [from_date, to_date])
        
        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 
        
        elif not from_date or not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 

        if location and not location == "each_location":
            results = Intervention.objects.filter(intervention_date__range = [from_date, to_date], location = location)

        elif not location and location == "each_location":
            results = Intervention.objects.all()[:50]
        
        elif not location and not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not location or not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.") 

        if hosting_agency and not hosting_agency == "each_hostingagency":
            results = Intervention.objects.filter(intervention_date__range = [from_date, to_date], hosting_agency = hosting_agency)
    
        elif not hosting_agency and hosting_agency == "each_hostingagency":
            results = Intervention.objects.all()

        elif not hosting_agency and not hosting_agency == "each_hostingagency":
            username = request.user.username

            messages.error(request, username + ", " + "hosting agency is not valid.")
        
        elif not hosting_agency or not hosting_agency == "each_hostingagency":
            username = request.user.username

            messages.error(request, username + ", " + "hosting agency is not valid.") 

        if not from_date and not to_date and not location and not hosting_agency:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        elif not from_date or not to_date or not location or not hosting_agency:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
        
        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter interventions within COTSEye to generate for reports today.")

        elif results is not None:
            try:
                interventions_count = results.count()

                interventions_label = "Interventions" + " Count"
            
            except:
                interventions_count = ""

                interventions_label = ""

            try:
                locations_count = results.count()

                locations_label = "Locations" + " Count"
            
            except:
                locations_count = ""

                locations_label = ""
            
            try:
                caughtamount_distribution = [str(caught_amount.caught_amount) for caught_amount in results]

                caughtamount_tally = Counter(caughtamount_distribution)

                caughtamount_frequency = caughtamount_tally.most_common(1)[0][0]

            except:
                caughtamount_frequency = ""
            
            try:
                caughtamount_firstfrequency = caughtamount_tally.most_common(1)[0][1]

                caughtamount_firstlabel = caughtamount_tally.most_common(1)[0][0] + " / Sqauare Meter Mode"

            except:
                caughtamount_firstfrequency = ""
            
                caughtamount_firstlabel = ""
            
            try:
                caughtamount_secondfrequency = caughtamount_tally.most_common(2)[1][1]

                caughtamount_secondlabel = caughtamount_tally.most_common(2)[1][0] + " / Sqauare Meter Mode"
            
            except:
                caughtamount_secondfrequency = ""
            
                caughtamount_secondlabel = ""
            
            try:
                caughtamount_thirdfrequency = caughtamount_tally.most_common(3)[2][1] 

                caughtamount_thirdlabel = caughtamount_tally.most_common(3)[2][0] + " / Sqauare Meter Mode"
            
            except:
                caughtamount_thirdfrequency = ""
            
                caughtamount_thirdlabel = ""
            
            try:
                hostingagency_distribution = [str(hosting_agency.hosting_agency) for hosting_agency in results]

                hostingagency_tally = Counter(hostingagency_distribution)

                hostingagency_frequency = hostingagency_tally.most_common(1)[0][0]

            except:
                hostingagency_frequency = ""
            
            try:
                hostingagency_firstfrequency = hostingagency_tally.most_common(1)[0][1]

                hostingagency_firstlabel = hostingagency_tally.most_common(1)[0][0] + " Mode"

            except:
                hostingagency_firstfrequency = ""
            
                hostingagency_firstlabel = ""
            
            try:
                hostingagency_secondfrequency = hostingagency_tally.most_common(2)[1][1]

                hostingagency_secondlabel = hostingagency_tally.most_common(2)[1][0] + " Mode"
            
            except:
                hostingagency_secondfrequency = ""
            
                hostingagency_secondlabel = ""
            
            try:
                hostingagency_thirdfrequency = hostingagency_tally.most_common(3)[2][1] 

                hostingagency_thirdlabel = hostingagency_tally.most_common(3)[2][0] + " Mode"
            
            except:
                hostingagency_thirdfrequency = ""
            
                hostingagency_thirdlabel = ""
                    
        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")


    context = {"username": username, "options": options, "records": records, "results": results, "interventions_count": interventions_count, "interventions_label": interventions_label, "locations_count": locations_count, "locations_label": locations_label, "caughtamount_frequency": caughtamount_frequency, "caughtamount_firstfrequency": caughtamount_firstfrequency, "caughtamount_firstlabel": caughtamount_firstlabel, "caughtamount_secondfrequency": caughtamount_secondfrequency, "caughtamount_secondlabel": caughtamount_secondlabel, "caughtamount_thirdfrequency": caughtamount_thirdfrequency, "caughtamount_thirdlabel": caughtamount_thirdlabel, "hostingagency_frequency": hostingagency_frequency, "hostingagency_firstfrequency": hostingagency_firstfrequency, "hostingagency_firstlabel": hostingagency_firstlabel, "hostingagency_secondfrequency": hostingagency_secondfrequency, "hostingagency_secondlabel": hostingagency_secondlabel, "hostingagency_thirdfrequency": hostingagency_thirdfrequency, "hostingagency_thirdlabel": hostingagency_thirdlabel}

    return render(request, "admin/control/intervention/intervention.html", context)


def ControlStatisticsStatusReadRedirect(request, object_id):
    object = Status.objects.get(id = object_id)
    
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 2:
            return redirect(reverse("officer:managements_status_change", kwargs = {"object_id": object.id}))

        elif usertype == 1:
            return redirect(reverse("admin:managements_status_change", kwargs = {"object_id": object.id}))
    
    else:
        return redirect(reverse("officer:managements_status_change", kwargs = {"object_id": object.id}))
    

def ControlStatisticsInterventionReadRedirect(request, object_id):
    usertype = request.user.usertype_id

    object = Intervention.objects.get(id = object_id)

    if request.user.is_authenticated:
        if usertype == 2:
            return redirect(reverse("officer:managements_intervention_change", kwargs = {"object_id": object.id}))

        elif usertype == 1:
            return redirect(reverse("admin:managements_intervention_change", kwargs = {"object_id": object.id}))
    
    else:
        return redirect(reverse("officer:managements_status_change", kwargs = {"object_id": object.id}))