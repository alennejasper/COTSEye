from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from authentications.views import ContributorCheck, OfficerCheck, AdministratorCheck
from managements.models import *


# Create your views here.
def PublicServiceStatus(request):
    username = "public/everyone"

    options = Status.objects.all()

    records = Status.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        results = None

        if from_date and to_date:
            results = Status.objects.filter(onset_date__range = [from_date, to_date])
        
        elif from_date and to_date and to_date < from_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = "public/everyone"
            
            messages.error(request, username + ", " + "Date range is not valid.")
        
        elif not from_date or not to_date:
            username = "public/everyone"

            messages.error(request, "date range is not valid.")
            
        if location and not location == "each_location":
            results = Status.objects.filter(location = location)

        elif not location and location == "each_location":
            results = Status.objects.filter(location = location)
        
        elif not location and not location == "each_location":
            username = "public/everyone"

            messages.error(request, username + ", " + "location is not valid.")
            
        elif not location or not location == "each_location":
            username = "public/everyone"

            messages.error(request, username + ", " + "location is not valid.")
        
        if statustype and not statustype == "each_statustype":
            results = Status.objects.filter(statustype = statustype)
            
        elif not statustype and statustype == "each_statustype":
            results = Status.objects.all()
        
        elif not statustype and not statustype == "each_statustype":
            username = "public/everyone"

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not statustype or not statustype == "each_statustype":
            username = "public/everyone"

            messages.error(request, username + ", " + "location is not valid.")

        if not from_date and not to_date and not location and not statustype:
            username = "public/everyone"

            messages.error(request, username + ", " + "information filter is not used within COTSEye.")
        
        elif not from_date or not to_date or not location or not statustype:
            username = "public/everyone"

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
        
        if results is None:
            username = "public/everyone"

            messages.info(request, username + ", " + "kindly filter statuses within COTSEye to generate for reports today.")

        elif not results:
            username = "public/everyone"

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "options": options, "records": records, "results": results}

    return render(request, "public/service/status/status.html", context)


def PublicServiceIntervention(request):
    username = "public/everyone"

    options = Intervention.objects.all()

    records = Intervention.objects.all()
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        location = request.GET.get("location")

        hosting_agency = request.GET.get("hosting_agency")

        results = None

        if from_date and to_date:
            results = Intervention.objects.filter(intervention_date__range = [from_date, to_date])
            
        elif from_date and to_date and to_date < from_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.")
        
        elif not from_date or not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.")

        if location and not location == "each_location":
            results = Intervention.objects.filter(location = location)

        elif not location and location == "each_location":
            results = Intervention.objects.all()
        
        elif not location and not location == "each_location":
            username = "public/everyone"

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not location or not location == "each_location":
            username = "public/everyone"

            messages.error(request, username + ", " + "location is not valid.")

        if hosting_agency and not hosting_agency == "each_hostingagency":
            results = Intervention.objects.filter(hosting_agency = hosting_agency)
    
        elif not hosting_agency and hosting_agency == "each_hostingagency":
            results = Intervention.objects.all()

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
            username = "public/everyone"

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
        
        if results is None:
            username = "public/everyone"

            messages.info(request, username + ", " + "kindly filter interventions within COTSEye to generate for reports today.")

        elif not results:
            username = "public/everyone"

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "options": options, "records": records, "results": results}

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

    records = Status.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        results = None

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

            messages.error(request, "date range is not valid.")
            
        if location and not location == "each_location":
            results = Status.objects.filter(location = location)

        elif not location and location == "each_location":
            results = Status.objects.filter(location = location)
        
        elif not location and not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
            
        elif not location or not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        if statustype and not statustype == "each_statustype":
            results = Status.objects.filter(statustype = statustype)
            
        elif not statustype and statustype == "each_statustype":
            results = Status.objects.all()
        
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
            username = request.user.username

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")
        
        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter interventions within COTSEye to generate for reports today.")

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "options": options, "records": records, "results": results}

    return render(request, "contributor/service/status/status.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceIntervention(request):
    username = request.user.username

    options = Intervention.objects.all()

    records = Intervention.objects.all()
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        location = request.GET.get("location")

        hosting_agency = request.GET.get("hosting_agency")

        results = None

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
            results = Intervention.objects.filter(location = location)[:50]

        elif not location and location == "each_location":
            results = Intervention.objects.all()[:50]
        
        elif not location and not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not location or not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")

        if hosting_agency and not hosting_agency == "each_hostingagency":
            results = Intervention.objects.filter(hosting_agency = hosting_agency)
    
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

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "options": options, "records": records, "results": results}

    return render(request, "contributor/service/intervention/intervention.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceInterventionRead(request, id):
    username = request.user.username

    intervention = Intervention.objects.filter(id = id)

    context = {"username": username, "intervention": intervention}

    return render(request, "contributor/service/intervention/read.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatisticsIntervention(request):
    username = request.user.username

    options = Intervention.objects.all()

    records = Intervention.objects.all()
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        location = request.GET.get("location")

        hosting_agency = request.GET.get("hosting_agency")

        results = None

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
            results = Intervention.objects.filter(location = location)

        elif not location and location == "each_location":
            results = Intervention.objects.all()
        
        elif not location and not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not location or not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.") 

        if hosting_agency and not hosting_agency == "each_hostingagency":
            results = Intervention.objects.filter(hosting_agency = hosting_agency)
    
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

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "options": options, "records": records, "results": results}

    return render(request, "officer/control/intervention/intervention.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatisticsStatus(request):
    username = request.user.username

    options = Status.objects.all()

    records = Status.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        results = None

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
            results = Status.objects.filter(location = location)

        elif not location and location == "each_location":
            results = Status.objects.filter(location = location)
        
        elif not location and not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not location or not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        if statustype and not statustype == "each_statustype":
            results = Status.objects.filter(statustype = statustype)
        
        elif not statustype and statustype == "each_statustype":
            results = Status.objects.all()
        
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

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")
    

    context = {"username": username, "options": options, "records": records, "results": results}

    return render(request, "officer/control/status/status.html", context)


@login_required(login_url = "Administrator Control Login")
@user_passes_test(AdministratorCheck, login_url = "Administrator Control Login")
def AdministratorControlStatisticsIntervention(request):
    username = request.user.username

    options = Intervention.objects.all()

    records = Intervention.objects.all()
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        location = request.GET.get("location")

        hosting_agency = request.GET.get("hosting_agency")

        results = None

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
            results = Intervention.objects.filter(location = location)

        elif not location and location == "each_location":
            results = Intervention.objects.all()
        
        elif not location and not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not location or not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.") 

        if hosting_agency and not hosting_agency == "each_hostingagency":
            results = Intervention.objects.filter(hosting_agency = hosting_agency)
    
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

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")


    context = {"username": username, "options": options, "records": records, "results": results}

    return render(request, "admin/control/intervention/intervention.html", context)


@login_required(login_url = "Administrator Control Login")
@user_passes_test(AdministratorCheck, login_url = "Administrator Control Login")
def AdministratorControlStatisticsStatus(request):
    username = request.user.username

    options = Status.objects.all()

    records = Status.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        location = request.GET.get("location")

        statustype = request.GET.get("statustype")

        results = None

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
            results = Status.objects.filter(location = location)

        elif not location and location == "each_location":
            results = Status.objects.filter(location = location)
        
        elif not location and not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        elif not location or not location == "each_location":
            username = request.user.username

            messages.error(request, username + ", " + "location is not valid.")
        
        if statustype and not statustype == "each_statustype":
            results = Status.objects.filter(statustype = statustype)
        
        elif not statustype and statustype == "each_statustype":
            results = Status.objects.all()
        
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

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")
    

    context = {"username": username, "options": options, "records": records, "results": results}

    return render(request, "admin/control/status/status.html", context)


def ControlStatisticsInterventionReadRedirect(request, object_id):
    usertype = request.user.usertype_id

    object = Intervention.objects.get(id = object_id)

    if usertype == 2:
        return redirect(reverse("officer:managements_intervention_change", kwargs = {"object_id": object.id}))

    if usertype == 1:
        return redirect(reverse("admin:managements_intervention_change", kwargs = {"object_id": object.id}))