from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse
from django.utils.encoding import smart_str
from auxiliaries.models import *
from authentications.views import ContributorCheck

# Create your views here.
def PublicServiceAnnouncement(request):
    username = "public/everyone"

    records = Announcement.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        results = None

        if from_date and to_date:
            results = Announcement.objects.filter(release_date__range = [from_date, to_date])
        
        elif not from_date or not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.") 
        
        elif from_date and to_date and to_date < from_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")

        if results is None:
            username = "public/everyone"

            messages.info(request, username + ", " + "kindly filter announcements within COTSEye to check for updates today.")

        elif not results:
            username = "public/everyone"

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results}

    return render(request, "public/service/announcement/announcement.html", context)


def PublicServiceAnnouncementRead(request, id):
    username = "public/everyone"

    announcement = Announcement.objects.filter(id = id)

    context = {"username": username, "announcement": announcement}

    return render(request, "public/service/announcement/read.html", context)


def PublicServiceResource(request):
    username = "public/everyone"

    resource_links = ResourceLink.objects.all()

    try:
        links_date = ResourceLink.objects.all().latest("resource__release_date")

        links_date = links_date.resource.release_date

    except:
        links_date = ""

    resource_files = ResourceFile.objects.all()

    try:
        files_date = ResourceFile.objects.all().latest("resource__release_date")

        files_date = files_date.resource.release_date
        
    except:
        files_date = ""
    
    context = {"username": username, "resource_links": resource_links, "links_date": links_date, "resource_files": resource_files, "files_date": files_date}
    
    return render(request, "public/service/resource/resource.html", context)


def PublicServiceResourceLink(request):
    username = "public/everyone"

    records = ResourceLink.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        results = None

        if from_date and to_date:
            results = ResourceLink.objects.filter(resource__release_date__range = [from_date, to_date])
        
        elif not from_date or not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.") 
        
        elif from_date and to_date and to_date < from_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")

        if results is None:
            username = "public/everyone"

            messages.info(request, username + ", " + "kindly filter resources within COTSEye to read for knowledge today.")

        elif not results:
            username = "public/everyone"

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results}
    
    return render(request, "public/service/resource/link.html", context)


def PublicServiceResourceFile(request):
    username = "public/everyone"

    records = ResourceFile.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        results = None

        if from_date and to_date:
            results = ResourceFile.objects.filter(resource__release_date__range = [from_date, to_date])
        
        elif not from_date or not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.") 
        
        elif from_date and to_date and to_date < from_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = "public/everyone"

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")

        if results is None:
            username = "public/everyone"

            messages.info(request, username + ", " + "kindly filter resources within COTSEye to read for knowledge today.")

        elif not results:
            username = "public/everyone"

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results}
    
    return render(request, "public/service/resource/file.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncement(request):
    username = request.user.username

    records = Announcement.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        results = None

        if from_date and to_date:
            results = Announcement.objects.filter(release_date__range = [from_date, to_date])

        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date or not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 

        elif not from_date and not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter announcements within COTSEye to check for updates today.")

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results}

    return render(request, "contributor/service/announcement/announcement.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceAnnouncementRead(request, id): 
    username = request.user.username

    announcement = Announcement.objects.filter(id = id)

    context = {"username": username, "announcement": announcement}

    return render(request, "contributor/service/announcement/read.html", context)


def ContributorServiceResource(request):
    username = request.user.username

    resource_links = ResourceLink.objects.all()

    try:
        links_date = ResourceLink.objects.latest("resource__release_date")
        
    except:
        links_date = ""

    resource_files = ResourceFile.objects.all()

    try:
        files_date = ResourceFile.objects.latest("resource__release_date")
        
    except:
        files_date = ""
    
    context = {"username": username, "resource_links": resource_links, "links_date": links_date, "resource_files": resource_files, "files_date": files_date}
    
    return render(request, "contributor/service/resource/resource.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceResourceLink(request):
    username = request.user.username

    records = ResourceLink.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        results = None

        if from_date and to_date:
            results = ResourceLink.objects.filter(resource__release_date__range = [from_date, to_date])
        
        elif not from_date or not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 
        
        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")

        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter resources within COTSEye to read for knowledge today.")

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results}
    
    return render(request, "contributor/service/resource/link.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceResourceFile(request):
    username = request.user.username

    records = ResourceFile.objects.all()

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        results = None

        if from_date and to_date:
            results = ResourceFile.objects.filter(resource__release_date__range = [from_date, to_date])
        
        elif not from_date or not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 
        
        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")

        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter resources within COTSEye to read for knowledge today.")

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results}
    
    return render(request, "contributor/service/resource/file.html", context)


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