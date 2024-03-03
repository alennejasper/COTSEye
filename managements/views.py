from django.shortcuts import render
from django.contrib import messages
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

    return render(request, "contributor/status/status.html", context)