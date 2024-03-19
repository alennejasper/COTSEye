from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from authentications.views import ContributorCheck, OfficerCheck, AdministratorCheck
from managements.models import *


# Create your views here.
def PublicServiceStatus(request):
    username = "public/everyone"

    options = Intervention.objects.all()

    statuses = Status.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        if "from_date" in request.GET or "to_date" in request.GET or "location" in request.GET or "statustype" in request.GET:
            if from_date and to_date:
                statuses = Status.objects.filter(onset_date__range = [from_date, to_date])

            elif not from_date and not to_date:
                username = "public/everyone"

                messages.error(request, username + ", " + "date range is not valid.")
            
            elif not from_date or not to_date:
                username = "public/everyone"

                messages.error(request, username + ", " + "date range is not valid.")

            if location and not location == "each_location":
                statuses = Status.objects.filter(location = location)[:50]

            elif not location and location == "each_location":
                statuses = Status.objects.all()[:50]
            
            elif not location and not location == "each_location":
                username = "public/everyone"

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not location or not location == "each_location":
                username = "public/everyone"

                messages.error(request, username + ", " + "location is not valid.")
            
            if statustype and not statustype == "each_statustype":
                statuses = Status.objects.filter(statustype = statustype)[:50]
            
            elif not statustype and statustype == "each_statustype":
                statuses = Status.objects.all()[:50]
            
            elif not statustype and not statustype == "each_statustype":
                username = "public/everyone"

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not statustype or not statustype == "each_statustype":
                username = "public/everyone"

                messages.error(request, username + ", " + "location is not valid.")

            if not from_date and not to_date and not location and not statustype:
                username = "public/everyone"

                messages.error(request, username + ", " + "information filter is empty within COTSEye.")
            
            elif not from_date or not to_date or not location or not statustype:
                username = "public/everyone"

                messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
    
    elif not statuses:
        username = "public/everyone"

        messages.info(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "options": options, "statuses": statuses}

    return render(request, "public/service/status/status.html", context)


def PublicServiceIntervention(request):
    username = "public/everyone"

    options = Intervention.objects.all()

    interventions = Intervention.objects.all()
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        location = request.GET.get("location")

        hosting_agency = request.GET.get("hosting_agency")

        if "from_date" in request.GET or "to_date" in request.GET or "location" in request.GET or "hosting_agency" in request.GET:
            if from_date and to_date:
                interventions = Intervention.objects.filter(intervention_date__range = [from_date, to_date])

            elif not from_date and not to_date:
                username = "public/everyone"

                messages.error(request, username + ", " + "date range is not valid.")
            
            elif not from_date or not to_date:
                username = "public/everyone"

                messages.error(request, username + ", " + "date range is not valid.")

            if location and not location == "each_location":
                interventions = Intervention.objects.filter(location = location)[:50]

            elif not location and location == "each_location":
                interventions = Intervention.objects.filter(location = location)[:50]
            
            elif not location and not location == "each_location":
                username = "public/everyone"

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not location or not location == "each_location":
                username = "public/everyone"

                messages.error(request, username + ", " + "location is not valid.")

            if hosting_agency and not hosting_agency == "each_hostingagency":
                interventions = Intervention.objects.filter(hosting_agency = hosting_agency)[:50]
        
            elif not hosting_agency and hosting_agency == "each_hostingagency":
                interventions = Intervention.objects.all()[:50]

            elif not hosting_agency and not hosting_agency == "each_hostingagency":
                username = "public/everyone"

                messages.error(request, username + ", " + "hosting agency is not valid.")
            
            elif not hosting_agency or not hosting_agency == "each_hostingagency":
                username = "public/everyone"

                messages.error(request, username + ", " + "hosting agency is not valid.")                      

            if not from_date and not to_date and not location and not hosting_agency:
                username = "public/everyone"

                messages.error(request, username + ", " + "information filter is empty within COTSEye.")
            
            elif not from_date or not to_date or not location or not hosting_agency:
                username = request.user.username

                messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")

    else:
        username = "public/everyone"

        messages.info(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "options": options, "interventions": interventions}

    return render(request, "public/service/intervention/intervention.html", context)


def PublicServiceInterventionRead(request, id):
    username = "public/everyone"
    
    intervention = Intervention.objects.filter(id = id)

    context = {"username": username, "intervention": intervention}

    return render(request, "public/service/intervention/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceStatus(request):
    username = request.user.username

    options = Status.objects.all()

    statuses = Status.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        if "from_date" in request.GET or "to_date" in request.GET or "location" in request.GET or "statustype" in request.GET:
            if from_date and to_date:
                statuses = Status.objects.filter(onset_date__range = [from_date, to_date], location = location, statustype = statustype)

            elif not from_date and not to_date:
                username = request.user.username
                
                messages.error(request, username + ", " + "Date range is not valid.")
            
            elif not from_date or not to_date:
                username = request.user.username

                messages.error(request, "Date range is not valid.")
            
            if location and not location == "each_location":
                statuses = Status.objects.filter(location = location)[:50]

            elif not location and location == "each_location":
                statuses = Status.objects.filter(location = location)[:50]
            
            elif not location and not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not location or not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            if statustype and not statustype == "each_statustype":
                statuses = Status.objects.filter(statustype = statustype)[:50]
            
            elif not statustype and statustype == "each_statustype":
                statuses = Status.objects.all()[:50]
            
            elif not statustype and not statustype == "each_statustype":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not statustype or not statustype == "each_statustype":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")

            if not from_date and not to_date and not location and not statustype:
                username = request.user.username

                messages.error(request, username + ", " + "information filter is not used within COTSEye.")
            
            elif not from_date or not to_date or not location or not statustype:
                username = "public/everyone"

                messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
    
    else:
        username = request.user.username

        messages.info(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "options": options, "statuses": statuses}

    return render(request, "contributor/service/status/status.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceIntervention(request):
    username = request.user.username

    options = Intervention.objects.all()

    interventions = Intervention.objects.all()
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        location = request.GET.get("location")

        hosting_agency = request.GET.get("hosting_agency")

        if "from_date" in request.GET or "to_date" in request.GET or "location" in request.GET or "hosting_agency" in request.GET:
            if from_date and to_date:
                interventions = Intervention.objects.filter(intervention_date__range = [from_date, to_date])

            elif not from_date and not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "date range is not valid.")
            
            elif not from_date or not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "date range is not valid.")

            if location and not location == "each_location":
                interventions = Intervention.objects.filter(location = location)[:50]

            elif not location and location == "each_location":
                interventions = Intervention.objects.all()[:50]
            
            elif not location and not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not location or not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")

            if hosting_agency and not hosting_agency == "each_hostingagency":
                interventions = Intervention.objects.filter(hosting_agency = hosting_agency)[:50]
        
            elif not hosting_agency and hosting_agency == "each_hostingagency":
                interventions = Intervention.objects.all()[:50]

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

    else:
        username = request.user.username

        messages.info(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "options": options, "interventions": interventions}

    return render(request, "contributor/service/intervention/intervention.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceInterventionRead(request, id):
    username = request.user.username

    intervention = Intervention.objects.filter(id = id)

    context = {"username": username, "intervention": intervention}

    return render(request, "contributor/service/intervention/read.html", context)


@login_required(login_url = "Officer Database Login")
@user_passes_test(OfficerCheck, login_url = "Officer Database Login")
def OfficerStatisticsIntervention(request):
    username = request.user.username

    options = Intervention.objects.all()

    interventions = Intervention.objects.all()[:50]
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        location = request.GET.get("location")

        hosting_agency = request.GET.get("hosting_agency")

        if "from_date" in request.GET or "to_date" in request.GET or "location" in request.GET or "hosting_agency" in request.GET:
            if from_date and to_date:
                interventions = Intervention.objects.filter(intervention_date__range = [from_date, to_date])[:50]

            elif not from_date and not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "date range is not valid.")
            
            elif not from_date or not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "date range is not valid.")

            if location and not location == "each_location":
                interventions = Intervention.objects.filter(location = location)[:50]

            elif not location and location == "each_location":
                interventions = Intervention.objects.all()[:50]
            
            elif not location and not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not location or not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")

            if hosting_agency and not hosting_agency == "each_hostingagency":
                interventions = Intervention.objects.filter(hosting_agency = hosting_agency)[:50]
        
            elif not hosting_agency and hosting_agency == "each_hostingagency":
                interventions = Intervention.objects.all()[:50]

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

    else:
        username = request.user.username

        messages.info(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "options": options, "interventions": interventions}

    return render(request, "officer/statistics/intervention/intervention.html", context)


@login_required(login_url = "Officer Database Login")
@user_passes_test(OfficerCheck, login_url = "Officer Database Login")
def OfficerStatisticsInterventionRead(request, id):
    username = request.user.username
    
    intervention = Intervention.objects.filter(id = id)

    context = {"username": username, "intervention": intervention}

    return render(request, "officer/statistics/intervention/read.html", context)


@login_required(login_url = "Officer Database Login")
@user_passes_test(OfficerCheck, login_url = "Officer Database Login")
def OfficerStatisticsStatus(request):
    username = request.user.username

    options = Status.objects.all()

    statuses = Status.objects.all()[:50]

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        if "from_date" in request.GET or "to_date" in request.GET or "location" in request.GET or "statustype" in request.GET:
            if from_date and to_date:
                statuses = Status.objects.filter(onset_date__range = [from_date, to_date])[:50]

            elif not from_date and not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "Date range is not valid.")
            
            elif not from_date or not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "Date range is not valid.")

            if location and not location == "each_location":
                statuses = Status.objects.filter(location = location)[:50]

            elif not location and location == "each_location":
                statuses = Status.objects.filter(location = location)[:50]
            
            elif not location and not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not location or not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            if statustype and not statustype == "each_statustype":
                statuses = Status.objects.filter(statustype = statustype)[:50]
            
            elif not statustype and statustype == "each_statustype":
                statuses = Status.objects.all()[:50]
            
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
                username = "public/everyone"

                messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
    
    elif not statuses:
        username = request.user.username

        messages.info(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "options": options, "statuses": statuses}

    return render(request, "officer/statistics/status/status.html", context)


@login_required(login_url = "Administrator Database Login")
@user_passes_test(AdministratorCheck, login_url = "Administrator Database Login")
def AdministratorStatisticsIntervention(request):
    username = request.user.username

    options = Intervention.objects.all()

    interventions = Intervention.objects.all()[:50]
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        location = request.GET.get("location")

        hosting_agency = request.GET.get("hosting_agency")

        if "from_date" in request.GET or "to_date" in request.GET or "location" in request.GET or "hosting_agency" in request.GET:
            if from_date and to_date:
                interventions = Intervention.objects.filter(intervention_date__range = [from_date, to_date])[:50]

            elif not from_date and not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "date range is not valid.") 
            
            elif not from_date or not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "date range is not valid.") 

            if location and not location == "each_location":
                interventions = Intervention.objects.filter(location = location)[:50]

            elif not location and location == "each_location":
                interventions = Intervention.objects.all()[:50]
            
            elif not location and not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not location or not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.") 

            if hosting_agency and not hosting_agency == "each_hostingagency":
                interventions = Intervention.objects.filter(hosting_agency = hosting_agency)[:50]
        
            elif not hosting_agency and hosting_agency == "each_hostingagency":
                interventions = Intervention.objects.all()[:50]

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

    else:
        username = request.user.username

        messages.info(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "options": options, "interventions": interventions}

    return render(request, "admin/statistics/intervention/intervention.html", context)


@login_required(login_url = "Administrator Database Login")
@user_passes_test(AdministratorCheck, login_url = "Administrator Database Login")
def AdministratorStatisticsInterventionRead(request, id):
    username = request.user.username
    
    intervention = Intervention.objects.filter(id = id)

    context = {"username": username, "intervention": intervention}

    return render(request, "admin/statistics/intervention/read.html", context)


@login_required(login_url = "Administrator Database Login")
@user_passes_test(AdministratorCheck, login_url = "Administrator Database Login")
def AdministratorStatisticsStatus(request):
    username = request.user.username

    options = Status.objects.all()

    statuses = Status.objects.all()[:50]

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        if "from_date" in request.GET or "to_date" in request.GET or "location" in request.GET or "statustype" in request.GET:
            if from_date and to_date:
                statuses = Status.objects.filter(onset_date__range = [from_date, to_date])[:50]

            elif not from_date and not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "Date range is not valid.")
            
            elif not from_date or not to_date:
                username = request.user.username

                messages.error(request, username + ", " + "Date range is not valid.")

            if location and not location == "each_location":
                statuses = Status.objects.filter(location = location)[:50]

            elif not location and location == "each_location":
                statuses = Status.objects.all()[:50]
            
            elif not location and not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            elif not location or not location == "each_location":
                username = request.user.username

                messages.error(request, username + ", " + "location is not valid.")
            
            if statustype and not statustype == "each_statustype":
                statuses = Status.objects.filter(statustype = statustype)[:50]
            
            elif not statustype and statustype == "each_statustype":
                statuses = Status.objects.all()[:50]
            
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
                username = "public/everyone"

                messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
    
    elif not statuses:
        username = request.user.username

        messages.info(request, username + ", " + "information input is empty within COTSEye.")

    context = {"username": username, "options": options, "statuses": statuses}

    return render(request, "admin/statistics/status/status.html", context)