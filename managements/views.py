from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from authentications.views import ContributorCheck
from managements.models import *


# Create your views here.
def PublicStatus(request):
    statuses = Status.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        barangay = request.GET.get("barangay")

        municipality = request.GET.get("municipality")

        if "from_date" in request.GET or "to_date" in request.GET or "barangay" in request.GET or "municipality" in request.GET:
            if from_date and to_date:
                statuses = Status.objects.filter(onset_date__range = [from_date, to_date], location__barangay = barangay, location__municipality = municipality)

                if not statuses:
                    username = "public/everyone"

                    messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

            elif not from_date and not to_date:
                messages.error(request, "Range is not valid.")
            
            elif not from_date or not to_date:
                messages.error(request, "Range is not valid.")

        elif not statuses:
            username = "public/everyone"

            messages.error(request, username + ", " + "information input is empty within COTSEye.")

    context = {"statuses": statuses}

    return render(request, "public/status/status.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorStatus(request):
    statuses = Status.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        barangay = request.GET.get("barangay")

        municipality = request.GET.get("municipality")

        if "from_date" in request.GET or "to_date" in request.GET or "barangay" in request.GET or "municipality" in request.GET:
            if from_date and to_date:
                statuses = Status.objects.filter(onset_date__range = [from_date, to_date], location__barangay = barangay, location__municipality = municipality)

                if not statuses:
                    username = request.user.username

                    messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

            elif not from_date and not to_date:
                messages.error(request, "Range is not valid.")
            
            elif not from_date or not to_date:
                messages.error(request, "Range is not valid.")

        elif not statuses:
            username = request.user.username

            messages.error(request, username + ", " + "information input is empty within COTSEye.")

    context = {"statuses": statuses}

    return render(request, "contributor/status/status.html", context)


def PublicIntervention(request):
    interventions = Intervention.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        if "from_date" in request.GET or "to_date" in request.GET:
            if from_date and to_date:
                interventions = Intervention.objects.filter(intervention_date__range = [from_date, to_date])
            
                if not interventions:
                    username = "public/everyone"

                    messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

            elif not from_date and not to_date:
                messages.error(request, "Range is not valid.")

            elif not from_date or not to_date:
                messages.error(request, "Range is not valid.")

        elif not interventions:
            username = "public/everyone"

            messages.error(request, username + ", " + "information input is empty within COTSEye.")

    context = {"interventions": interventions}

    return render(request, "public/intervention/intervention.html", context)


def PublicInterventionRead(request, id):
    intervention = Intervention.objects.filter(id = id)

    context = {"intervention": intervention}

    return render(request, "public/intervention/read.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorIntervention(request):
    interventions = Intervention.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        if "from_date" in request.GET or "to_date" in request.GET:
            if from_date and to_date:
                interventions = Intervention.objects.filter(intervention_date__range = [from_date, to_date])
            
                if not interventions:
                    username = request.user.username

                    messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

            elif not from_date and not to_date:
                messages.error(request, "Range is not valid.")

            elif not from_date or not to_date:
                messages.error(request, "Range is not valid.")

        elif not interventions:
            username = request.user.username

            messages.error(request, username + ", " + "information input is empty within COTSEye.")

    context = {"interventions": interventions}

    return render(request, "contributor/intervention/intervention.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorInterventionRead(request, id):
    intervention = Intervention.objects.filter(id = id)

    context = {"intervention": intervention}

    return render(request, "contributor/intervention/read.html", context)