from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse
from authentications.views import ContributorCheck, OfficerCheck, AdministratorCheck
from collections import Counter
from managements.models import *

import datetime

# Create your views here.
def PublicServiceIntervention(request):
    username = "public/everyone"

    interventions = Intervention.objects.all()

    context = {"username": username, "interventions": interventions}

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

    interventions = Intervention.objects.all()

    context = {"username": username, "interventions": interventions}

    return render(request, "contributor/service/intervention/intervention.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceInterventionRead(request, id):
    username = request.user.username

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    intervention = Intervention.objects.get(id = id)

    context = {"username": username, "scheme": scheme, "host": host, "intervention": intervention}

    return render(request, "contributor/service/intervention/read.html", context)


@login_required(login_url = "officer:Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "officer:Officer Control Login")
def OfficerControlStatisticsIntervention(request):
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

    return render(request, "officer/control/intervention/intervention.html", context)


@login_required(login_url = "officer:Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "officer:Officer Control Login")
def OfficerControlStatisticsStatus(request):
    username = request.user.username

    options = Status.objects.all()

    records = Status.objects.all()

    results = None

    try:
        statuses_count = records.count()

        statuses_label = "Statuses" + " Count"
    
    except:
        statuses_count = ""

        statuses_label = ""
    
    try:
        caughtoverall_count = sum(caught_overall.caught_overall for caught_overall in records)

        caughtoverall_label = "Caught Overall" + " Count"
    
    except:
        caughtoverall_count = ""

        caughtoverall_label = ""
    
    try:
        location_distribution = [str(location.location) for location in records]

        location_tally = Counter(location_distribution)

        location_frequency = location_tally.most_common(1)[0][0]

    except:
        location_frequency = ""

    try:
        location_firstfrequency = location_tally.most_common(1)[0][1]

        location_firstlabel = location_tally.most_common(1)[0][0] + " Frequency"

    except:
        location_firstfrequency = ""
    
        location_firstlabel = ""

    try:
        location_secondfrequency = location_tally.most_common(2)[1][1]

        location_secondlabel = location_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        location_secondfrequency = ""
    
        location_secondlabel = ""

    try:
        location_thirdfrequency = location_tally.most_common(3)[2][1] 

        location_thirdlabel = location_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        location_thirdfrequency = ""
    
        location_thirdlabel = ""
    
    try:
        statustype_distribution = [str(statustype.statustype) for statustype in records]

        statustype_tally = Counter(statustype_distribution)

        statustype_frequency = statustype_tally.most_common(1)[0][0]

    except:
        statustype_frequency = ""

    try:
        statustype_firstfrequency = statustype_tally.most_common(1)[0][1]

        statustype_firstlabel = statustype_tally.most_common(1)[0][0] + " Frequency"

    except:
        statustype_firstfrequency = ""
    
        statustype_firstlabel = ""

    try:
        statustype_secondfrequency = statustype_tally.most_common(2)[1][1]

        statustype_secondlabel = statustype_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        statustype_secondfrequency = ""
    
        statustype_secondlabel = ""

    try:
        statustype_thirdfrequency = statustype_tally.most_common(3)[2][1] 

        statustype_thirdlabel = statustype_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        statustype_thirdfrequency = ""
    
        statustype_thirdlabel = ""

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        if from_date and to_date:
            results = Status.objects.filter(onset_date__range = [from_date, to_date])

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
            results = Status.objects.filter(onset_date__range = [from_date, to_date], location = location)

        elif not location and location == "each_location":
            results = Status.objects.filter(onset_date__range = [from_date, to_date], location = location)
        
        elif not location and not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not location or not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        if statustype and not statustype == "each_statustype":
            results = Status.objects.filter(statustype = statustype)
        
        elif not statustype and statustype == "each_statustype":
            results = Status.objects.all()[:50]
        
        elif not statustype and not statustype == "each_statustype":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not statustype or not statustype == "each_statustype":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")

        if not from_date and not to_date and not location and not statustype:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        elif not from_date or not to_date or not location or not statustype:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
        
        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter statuses within COTSEye to generate for reports today.")

        elif results is not None:
            try:
                statuses_count = results.count()

                statuses_label = "Statuses" + " Count"
            
            except:
                statuses_count = ""

                statuses_label = ""
            
            try:
                caughtoverall_count = sum(caught_overall.caught_overall for caught_overall in results)

                caughtoverall_label = "Caught Overall" + " Count"
            
            except:
                caughtoverall_count = ""

                caughtoverall_label = ""
            
            try:
                location_distribution = [str(location.location) for location in results]

                location_tally = Counter(location_distribution)

                location_frequency = location_tally.most_common(1)[0][0]

            except:
                location_frequency = ""

            try:
                location_firstfrequency = location_tally.most_common(1)[0][1]

                location_firstlabel = location_tally.most_common(1)[0][0] + " Frequency"

            except:
                location_firstfrequency = ""
            
                location_firstlabel = ""

            try:
                location_secondfrequency = location_tally.most_common(2)[1][1]

                location_secondlabel = location_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                location_secondfrequency = ""
            
                location_secondlabel = ""

            try:
                location_thirdfrequency = location_tally.most_common(3)[2][1] 

                location_thirdlabel = location_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                location_thirdfrequency = ""
            
                location_thirdlabel = ""
            
            try:
                statustype_distribution = [str(statustype.statustype) for statustype in results]

                statustype_tally = Counter(statustype_distribution)

                statustype_frequency = statustype_tally.most_common(1)[0][0]

            except:
                statustype_frequency = ""

            try:
                statustype_firstfrequency = statustype_tally.most_common(1)[0][1]

                statustype_firstlabel = statustype_tally.most_common(1)[0][0] + " Frequency"

            except:
                statustype_firstfrequency = ""
            
                statustype_firstlabel = ""

            try:
                statustype_secondfrequency = statustype_tally.most_common(2)[1][1]

                statustype_secondlabel = statustype_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                statustype_secondfrequency = ""
            
                statustype_secondlabel = ""

            try:
                statustype_thirdfrequency = statustype_tally.most_common(3)[2][1] 

                statustype_thirdlabel = statustype_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                statustype_thirdfrequency = ""
            
                statustype_thirdlabel = ""
    
        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")
    

    context = {"username": username, "options": options, "records": records, "results": results, "statuses_count": statuses_count, "statuses_label": statuses_label, "caughtoverall_count": caughtoverall_count, "caughtoverall_label": caughtoverall_label, "location_frequency": location_frequency, "location_firstfrequency": location_firstfrequency, "location_firstlabel": location_firstlabel, "location_secondfrequency": location_secondfrequency, "location_secondlabel": location_secondlabel, "location_thirdfrequency": location_thirdfrequency, "location_thirdlabel": location_thirdlabel, "statustype_frequency": statustype_frequency, "statustype_firstfrequency": statustype_firstfrequency, "statustype_firstlabel": statustype_firstlabel, "statustype_secondfrequency": statustype_secondfrequency, "statustype_secondlabel": statustype_secondlabel, "statustype_thirdfrequency": statustype_thirdfrequency, "statustype_thirdlabel": statustype_thirdlabel}

    return render(request, "officer/control/status/status.html", context)


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


@login_required(login_url = "admin:Administrator Control Login")
@user_passes_test(AdministratorCheck, login_url = "admin:Administrator Control Login")
def AdministratorControlStatisticsStatus(request):
    username = request.user.username

    options = Status.objects.all()

    records = Status.objects.all()

    results = None

    try:
        statuses_count = records.count()

        statuses_label = "Statuses" + " Count"
    
    except:
        statuses_count = ""

        statuses_label = ""
    
    try:
        caughtoverall_count = sum(caught_overall.caught_overall for caught_overall in records)

        caughtoverall_label = "Caught Overall" + " Count"
    
    except:
        caughtoverall_count = ""

        caughtoverall_label = ""
    
    try:
        location_distribution = [str(location.location) for location in records]

        location_tally = Counter(location_distribution)

        location_frequency = location_tally.most_common(1)[0][0]

    except:
        location_frequency = ""

    try:
        location_firstfrequency = location_tally.most_common(1)[0][1]

        location_firstlabel = location_tally.most_common(1)[0][0] + " Frequency"

    except:
        location_firstfrequency = ""
    
        location_firstlabel = ""

    try:
        location_secondfrequency = location_tally.most_common(2)[1][1]

        location_secondlabel = location_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        location_secondfrequency = ""
    
        location_secondlabel = ""

    try:
        location_thirdfrequency = location_tally.most_common(3)[2][1] 

        location_thirdlabel = location_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        location_thirdfrequency = ""
    
        location_thirdlabel = ""
    
    try:
        statustype_distribution = [str(statustype.statustype) for statustype in records]

        statustype_tally = Counter(statustype_distribution)

        statustype_frequency = statustype_tally.most_common(1)[0][0]

    except:
        statustype_frequency = ""

    try:
        statustype_firstfrequency = statustype_tally.most_common(1)[0][1]

        statustype_firstlabel = statustype_tally.most_common(1)[0][0] + " Frequency"

    except:
        statustype_firstfrequency = ""
    
        statustype_firstlabel = ""

    try:
        statustype_secondfrequency = statustype_tally.most_common(2)[1][1]

        statustype_secondlabel = statustype_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        statustype_secondfrequency = ""
    
        statustype_secondlabel = ""

    try:
        statustype_thirdfrequency = statustype_tally.most_common(3)[2][1] 

        statustype_thirdlabel = statustype_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        statustype_thirdfrequency = ""
    
        statustype_thirdlabel = ""

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        if from_date and to_date:
            results = Status.objects.filter(onset_date__range = [from_date, to_date])

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
            results = Status.objects.filter(onset_date__range = [from_date, to_date], location = location)

        elif not location and location == "each_location":
            results = Status.objects.all()[:50]
        
        elif not location and not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not location or not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        if statustype and not statustype == "each_statustype":
            results = Status.objects.filter(statustype = statustype)
        
        elif not statustype and statustype == "each_statustype":
            results = Status.objects.all()[:50]
        
        elif not statustype and not statustype == "each_statustype":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not statustype or not statustype == "each_statustype":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")

        if not from_date and not to_date and not location and not statustype:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        elif not from_date or not to_date or not location or not statustype:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
        
        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter statuses within COTSEye to generate for reports today.")

        elif results is not None:
            try:
                statuses_count = results.count()

                statuses_label = "Statuses" + " Count"
            
            except:
                statuses_count = ""

                statuses_label = ""
            
            try:
                caughtoverall_count = sum(caught_overall.caught_overall for caught_overall in results)

                caughtoverall_label = "Caught Overall" + " Count"
            
            except:
                caughtoverall_count = ""

                caughtoverall_label = ""
            
            try:
                location_distribution = [str(location.location) for location in results]

                location_tally = Counter(location_distribution)

                location_frequency = location_tally.most_common(1)[0][0]

            except:
                location_frequency = ""

            try:
                location_firstfrequency = location_tally.most_common(1)[0][1]

                location_firstlabel = location_tally.most_common(1)[0][0] + " Frequency"

            except:
                location_firstfrequency = ""
            
                location_firstlabel = ""

            try:
                location_secondfrequency = location_tally.most_common(2)[1][1]

                location_secondlabel = location_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                location_secondfrequency = ""
            
                location_secondlabel = ""

            try:
                location_thirdfrequency = location_tally.most_common(3)[2][1] 

                location_thirdlabel = location_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                location_thirdfrequency = ""
            
                location_thirdlabel = ""
            
            try:
                statustype_distribution = [str(statustype.statustype) for statustype in results]

                statustype_tally = Counter(statustype_distribution)

                statustype_frequency = statustype_tally.most_common(1)[0][0]

            except:
                statustype_frequency = ""

            try:
                statustype_firstfrequency = statustype_tally.most_common(1)[0][1]

                statustype_firstlabel = statustype_tally.most_common(1)[0][0] + " Frequency"

            except:
                statustype_firstfrequency = ""
            
                statustype_firstlabel = ""

            try:
                statustype_secondfrequency = statustype_tally.most_common(2)[1][1]

                statustype_secondlabel = statustype_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                statustype_secondfrequency = ""
            
                statustype_secondlabel = ""

            try:
                statustype_thirdfrequency = statustype_tally.most_common(3)[2][1] 

                statustype_thirdlabel = statustype_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                statustype_thirdfrequency = ""
            
                statustype_thirdlabel = ""
    
        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")
    

    context = {"username": username, "options": options, "records": records, "results": results, "statuses_count": statuses_count, "statuses_label": statuses_label, "caughtoverall_count": caughtoverall_count, "caughtoverall_label": caughtoverall_label, "location_frequency": location_frequency, "location_firstfrequency": location_firstfrequency, "location_firstlabel": location_firstlabel, "location_secondfrequency": location_secondfrequency, "location_secondlabel": location_secondlabel, "location_thirdfrequency": location_thirdfrequency, "location_thirdlabel": location_thirdlabel, "statustype_frequency": statustype_frequency, "statustype_firstfrequency": statustype_firstfrequency, "statustype_firstlabel": statustype_firstlabel, "statustype_secondfrequency": statustype_secondfrequency, "statustype_secondlabel": statustype_secondlabel, "statustype_thirdfrequency": statustype_thirdfrequency, "statustype_thirdlabel": statustype_thirdlabel}

    return render(request, "admin/control/status/status.html", context)

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