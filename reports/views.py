from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from authentications.models import Account
from authentications.views import ContributorCheck, OfficerCheck, AdministratorCheck
from collections import Counter
from reports.models import *
from reports.forms import CoordinatesForm, PostObservationForm, PostForm

import datetime


# Create your views here.
def PublicServicePostValidRead(request, id):
    username = request.user.username

    valid_post = Post.objects.get(id = id, post_status = 1)
    
    context = {"username": username, "valid_post": valid_post}
    
    return render(request, "public/service/post/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceReport(request):
    username = request.user.username

    context = {"username": username}
    
    return render(request, "contributor/service/report/report.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceReportCapture(request):
    username = request.user.username

    coordinates_form = CoordinatesForm()

    postobservation_form = PostObservationForm()

    depths = Depth.objects.all()

    weathers = Weather.objects.all()

    post_form = PostForm()
    
    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST)

        postobservation_form = PostObservationForm(request.POST)

        post_form =  PostForm(request.POST, request.FILES)

        if coordinates_form.is_valid() and postobservation_form.is_valid() and post_form.is_valid():
            coordinates = coordinates_form.save(commit = False)

            post_observation = postobservation_form.save(commit = False)

            post = post_form.save(commit = False)

            user = request.user.user

            post_status = PostStatus.objects.get(id = 3)

            coordinates = Coordinates.objects.create(latitude = coordinates.latitude, longitude = coordinates.longitude)
            
            depth = request.POST.get("depth")

            try:
                post_observation.depth = Depth.objects.get(id = depth)

            except:
                post_observation.depth = None

            weather = request.POST.get("weather")

            try:
                post_observation.weather = Weather.objects.get(id = weather)
            
            except:
                post_observation.weather = None

            post_observation = PostObservation.objects.create(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather)
            
            if Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and PostObservation.objects.filter(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather).exists():
                post = Post.objects.create(user = user, description = post.description, capture_date = post.capture_date, coordinates = coordinates, post_status = post_status, post_observation = post_observation)

                post_photos = request.FILES.getlist("post_photos")

                for post_photo in post_photos:
                    photo = PostPhoto.objects.create(post_photo = post_photo)
                    
                    post.post_photos.add(photo)
                
                officers = User.objects.filter(account__usertype_id = 2)

                for officer in officers:
                    subject = "COTSEye has been delivered an alert message!"

                    scheme = request.scheme

                    host = request.META["HTTP_HOST"]

                    template = render_to_string("admin/control/email/email.html", {"officer": officer.account.username, "contributor": post.user.account.username, "post": post, "scheme": scheme, "host": host})

                    body = strip_tags(template)

                    source = "COTSEye <settings.EMAIL_HOST_USER>"

                    recipient = [officer.email]

                    email = EmailMultiAlternatives(
                        subject,
                        
                        body,
                        
                        source,
                        
                        recipient,
                    )

                    email.attach_alternative(template, "text/html")

                    email.fail_silently = False

                    email.send()

                username = request.user.username
                
                messages.success(request, username + ", " + "your information input was recorded for COTSEye.")
                
                return redirect("Contributor Service Home")
        
        else:
            messages.error(request, "Information input is not valid.")
            
            messages.error(request, coordinates_form.errors, postobservation_form.errors, post_form.errors)

    else:
        coordinates_form = CoordinatesForm()
        
        postobservation_form = PostObservationForm()
        
        post_form = PostForm() 

    context = {"username": username, "coordinates_form": coordinates_form, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/service/report/capture.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceReportChoose(request):
    username = request.user.username

    coordinates_form = CoordinatesForm()

    postobservation_form = PostObservationForm()

    depths = Depth.objects.all()

    weathers = Weather.objects.all()

    post_form = PostForm()
    
    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST)

        postobservation_form = PostObservationForm(request.POST)

        post_form =  PostForm(request.POST, request.FILES)

        if coordinates_form.is_valid() and post_form.is_valid() and postobservation_form.is_valid():
            coordinates = coordinates_form.save(commit = False)

            post_observation = postobservation_form.save(commit = False)

            post = post_form.save(commit = False)

            user = request.user.user

            post_status = PostStatus.objects.get(id = 3)

            coordinates = Coordinates.objects.create(latitude = coordinates.latitude, longitude = coordinates.longitude)
            
            depth = request.POST.get("depth")

            try:
                post_observation.depth = Depth.objects.get(id = depth)

            except:
                post_observation.depth = None

            weather = request.POST.get("weather")

            try:
                post_observation.weather = Weather.objects.get(id = weather)
            
            except:
                post_observation.weather = None

            post_observation = PostObservation.objects.create(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather)
            
            if Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and PostObservation.objects.filter(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather).exists():
                post = Post.objects.create(user = user, description = post.description, capture_date = post.capture_date, coordinates = coordinates, post_status = post_status, post_observation = post_observation)

                post_photos = request.FILES.getlist("post_photos")
        
                for post_photo in post_photos:
                    photo = PostPhoto.objects.create(post_photo = post_photo)
                    
                    post.post_photos.add(photo)
                
                officers = User.objects.filter(account__usertype_id = 2)

                for officer in officers:
                    subject = "COTSEye has delivered an alert message!"

                    scheme = request.scheme

                    host = request.META["HTTP_HOST"]

                    template = render_to_string("admin/control/email/email.html", {"officer": officer.account.username, "contributor": post.user.account.username, "post": post, "scheme": scheme, "host": host})

                    body = strip_tags(template)

                    source = "COTSEye <settings.EMAIL_HOST_USER>"

                    recipient = [officer.email]

                    email = EmailMultiAlternatives(
                        subject,
                        
                        body,
                        
                        source,
                        
                        recipient,
                    )

                    email.attach_alternative(template, "text/html")

                    email.fail_silently = False

                    email.send()

                username = request.user.username
                
                messages.success(request, username + ", " + "your information input was recorded for COTSEye.")
                
                return redirect("Contributor Service Home")
        
        else:
            messages.error(request, "Information input is not valid.")
            
            messages.error(request, coordinates_form.errors, postobservation_form.errors, post_form.errors)

    else:
        coordinates_form = CoordinatesForm()
        
        postobservation_form = PostObservationForm()
        
        post_form = PostForm() 

    context = {"username": username, "coordinates_form": coordinates_form, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/service/report/choose.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceReportCaptureUpdate(request, id):
    username = request.user.username

    uncertain_post = Post.objects.get(id = id, post_status = 3)   

    depths = Depth.objects.all()

    weathers = Weather.objects.all()

    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST, instance = uncertain_post.coordinates)
        
        postobservation_form = PostObservationForm(request.POST, instance = uncertain_post.post_observation)
        
        post_form =  PostForm(request.POST, request.FILES, instance = uncertain_post)

        if coordinates_form.is_valid() and postobservation_form.is_valid() and post_form.is_valid():
            coordinates_form.save()
            
            postobservation_form.save()
           
            post = post_form.save()

            for post_photo in uncertain_post.post_photos.all():
                post_photo.delete()

            post_photos = request.FILES.getlist("post_photo")

            for post_photo in post_photos:
                photo = PostPhoto.objects.create(post_photo = post_photo)

                post.post_photos.add(photo)

            username = request.user.username
            
            messages.success(request, username + ", " + "your information input was updated for COTSEye.")
            
            return redirect("Contributor Service Post Uncertain")

        else:
            messages.error(request, "Information input is not valid.")
            
            messages.error(request, coordinates_form.errors, postobservation_form.errors, post_form.errors)
        
    else:
        coordinates_form = CoordinatesForm(instance = uncertain_post.coordinates)
        
        postobservation_form = PostObservationForm(instance = uncertain_post.post_observation)
        
        post_form = PostForm(instance = uncertain_post)       

    context = {"username": username, "uncertain_post": uncertain_post, "coordinates_form": coordinates_form, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/service/report/capture.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceReportChooseUpdate(request, id):
    username = request.user.username

    uncertain_post = Post.objects.get(id = id, post_status = 3)   

    depths = Depth.objects.all()

    weathers = Weather.objects.all()

    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST, instance = uncertain_post.coordinates)
        
        postobservation_form = PostObservationForm(request.POST, instance = uncertain_post.post_observation)
        
        post_form =  PostForm(request.POST, request.FILES, instance = uncertain_post)

        if coordinates_form.is_valid() and postobservation_form.is_valid() and post_form.is_valid():
            coordinates_form.save()
            
            postobservation_form.save()
           
            post = post_form.save()

            for post_photo in uncertain_post.post_photos.all():
                post_photo.delete()
                
            post_photos = request.FILES.getlist("post_photo")

            for post_photo in post_photos:
                photo = PostPhoto.objects.create(post_photo = post_photo)

                post.post_photos.add(photo)

            username = request.user.username
            
            messages.success(request, username + ", " + "your information input was updated for COTSEye.")
            
            return redirect("Contributor Service Post Uncertain")

        else:
            messages.error(request, "Information input is not valid.")
            
            messages.error(request, coordinates_form.errors, postobservation_form.errors, post_form.errors)
        
    else:
        coordinates_form = CoordinatesForm(instance = uncertain_post.coordinates)
        
        postobservation_form = PostObservationForm(instance = uncertain_post.post_observation)
        
        post_form = PostForm(instance = uncertain_post)       

    context = {"username": username, "uncertain_post": uncertain_post, "coordinates_form": coordinates_form, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/service/report/choose.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePost(request):
    username = request.user.username

    valid_posts = Post.objects.filter(user = request.user.user, post_status = 1)

    try:
        valid_date = Post.objects.filter(user = request.user.user, post_status = 1).latest("capture_date")
        
    except:
        valid_date = None

    invalid_posts = Post.objects.filter(user = request.user.user, post_status = 2)

    try:
        invalid_date = Post.objects.filter(user = request.user.user, post_status = 2).latest("capture_date")
        
    except:
        invalid_date = None

    uncertain_posts = Post.objects.filter(user = request.user.user, post_status = 3)

    try:
        uncertain_date = Post.objects.filter(user = request.user.user, post_status = 3).latest("capture_date")

    except:
        uncertain_date = None
    
    context = {"username": username, "valid_posts": valid_posts, "valid_date": valid_date, "invalid_posts": invalid_posts, "invalid_date": invalid_date, "uncertain_posts": uncertain_posts, "uncertain_date": uncertain_date}
    
    return render(request, "contributor/service/post/post.html", context)

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostValid(request):
    username = request.user.username

    options = Post.objects.all()

    records = Post.objects.filter(user = request.user.user, post_status = 1)

    results = None
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        depth = request.GET.get("depth")

        weather = request.GET.get("weather")

        if from_date and to_date:
            results = Post.objects.filter(user = request.user.user, post_status = 1, capture_date__range = [from_date, to_date])

        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")
        
        elif not from_date and not to_date:
            messages.error(request, "Date range is not valid.")

        elif not from_date or not to_date:
            messages.error(request, "Date range is not valid.")
        
        if depth and not depth == "each_depth":
            results = Post.objects.filter(user = request.user.user, post_status = 1, post_observation__depth = depth)
    
        elif not depth and depth == "each_depth":
            results = Post.objects.filter(user = request.user.user, post_status = 1)

        elif not depth and not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")
        
        elif not depth or not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")

        if weather and not weather == "each_weather":
            results = Post.objects.filter(user = request.user.user, post_status = 1, post_observation__weather = weather)
    
        elif not weather and weather == "each_weather":
            results = Post.objects.filter(user = request.user.user, post_status = 1)

        elif not weather and not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")
        
        elif not weather or not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")  

        if not from_date and not to_date and not depth and not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        elif not from_date or not to_date or not depth or not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")

        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter posts within COTSEye to generate for reports today.")

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results, "options": options}
    
    return render(request, "contributor/service/post/valid.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostValidRead(request, id):
    username = request.user.username

    valid_post = Post.objects.get(id = id, user = request.user.user, post_status = 1)
    
    context = {"username": username, "valid_post": valid_post}
    
    return render(request, "contributor/service/post/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostInvalid(request):  
    username = request.user.username

    options = Post.objects.all()
    
    records = Post.objects.filter(user = request.user.user, post_status = 2)

    results = None
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        depth = request.GET.get("depth")

        weather = request.GET.get("weather")

        if from_date and to_date:
            results = Post.objects.filter(user = request.user.user, post_status = 2, capture_date__range = [from_date, to_date])

        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")
        
        elif not from_date and not to_date:
            messages.error(request, "Date range is not valid.")

        elif not from_date or not to_date:
            messages.error(request, "Date range is not valid.")
        
        if depth and not depth == "each_depth":
            results = Post.objects.filter(user = request.user.user, post_status = 2, post_observation__depth = depth)
    
        elif not depth and depth == "each_depth":
            results = Post.objects.filter(user = request.user.user, post_status = 2)

        elif not depth and not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")
        
        elif not depth or not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")

        if weather and not weather == "each_weather":
            results = Post.objects.filter(user = request.user.user, post_status = 2, post_observation__weather = weather)
    
        elif not weather and weather == "each_weather":
            results = Post.objects.filter(user = request.user.user, post_status = 2)

        elif not weather and not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")
        
        elif not weather or not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")  

        if not from_date and not to_date and not depth and not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        elif not from_date or not to_date or not depth or not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")

        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter posts within COTSEye to generate for reports today.")

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results, "options": options}
    
    return render(request, "contributor/service/post/invalid.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostInvalidRead(request, id):
    username = request.user.username

    invalid_post = Post.objects.get(id = id, user = request.user.user, post_status = 2)
    
    context = {"username": username, "invalid_post": invalid_post}
    
    return render(request, "contributor/service/post/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostInvalidDelete(request, id):
    invalid_post = Post.objects.get(id = id, post_status = 2)

    if invalid_post.user == request.user.user:
        description = invalid_post.description

        coordinates = invalid_post.coordinates

        delete_post = Post.objects.filter(Q(description = description) & Q(coordinates = coordinates) & Q(post_status = 2))

        for invalid_post in delete_post:
            invalid_post.coordinates.delete()
        
            invalid_post.post_observation.delete()
        
            invalid_post.delete()

        username = request.user.username
        
        messages.success(request, username + ", " + "your information input was vanished from COTSEye.")
            
        return redirect("Contributor Service Post Invalid")

    else:
        messages.error(request, "Information input may not be vanished.")

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostUncertain(request):
    username = request.user.username

    options = Post.objects.all()

    records = Post.objects.filter(user = request.user.user, post_status = 3)

    results = None
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        depth = request.GET.get("depth")

        weather = request.GET.get("weather")

        if from_date and to_date:
            results = Post.objects.filter(user = request.user.user, post_status = 3, capture_date__range = [from_date, to_date])

        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")
        
        elif not from_date and not to_date:
            messages.error(request, "Date range is not valid.")

        elif not from_date or not to_date:
            messages.error(request, "Date range is not valid.")
        
        if depth and not depth == "each_depth":
            results = Post.objects.filter(user = request.user.user, post_status = 3, post_observation__depth = depth)
    
        elif not depth and depth == "each_depth":
            results = Post.objects.filter(user = request.user.user, post_status = 3)

        elif not depth and not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")
        
        elif not depth or not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")

        if weather and not weather == "each_weather":
            results = Post.objects.filter(user = request.user.user, post_status = 3, post_observation__weather = weather)
    
        elif not weather and weather == "each_weather":
            results = Post.objects.filter(user = request.user.user, post_status = 3)

        elif not weather and not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")
        
        elif not weather or not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")  

        if not from_date and not to_date and not depth and not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        elif not from_date or not to_date or not depth or not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")

        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter posts within COTSEye to generate for reports today.")

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "records": records, "results": results, "options": options}

    return render(request, "contributor/service/post/uncertain.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostUncertainRead(request, id):
    username = request.user.username

    uncertain_post = Post.objects.get(id = id, user = request.user.user, post_status = 3)
    
    context = {"username": username, "uncertain_post": uncertain_post}
    
    return render(request, "contributor/service/post/read.html", context)


@login_required(login_url = "officer:Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "officer:Officer Control Login")
def OfficerControlStatisticsPost(request):
    username = request.user.username

    options = Post.objects.all()

    records = Post.objects.all()

    results = None

    try:
        posts_count = records.count()

        posts_label = "Posts" + " Count"
    
    except:
        posts_count = ""

        posts_label = ""

    try:
        users_count = records.values("user").distinct().count()

        users_label = "Users" + " Count"
    
    except:
        users_count = ""

        users_label = ""

    try:
        user_distribution = [str(user.user) for user in records]

        user_tally = Counter(user_distribution)
        
        user_frequency = user_tally.most_common(1)[0][0]
    
    except:
        user_frequency = ""
    
    try:
        user_firstfrequency = user_tally.most_common(1)[0][1]

        user_firstlabel = user_tally.most_common(1)[0][0] + " Frequency"

    except:
        user_firstfrequency = ""
    
        user_firstlabel = ""
    
    try:
        user_secondfrequency = user_tally.most_common(2)[1][1]

        user_secondlabel = user_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        user_secondfrequency = ""
    
        user_secondlabel = ""
    
    try:
        user_thirdfrequency = size_tally.most_common(3)[2][1] 

        user_thirdlabel = size_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        user_thirdfrequency = ""
    
        user_thirdlabel = ""

    try:
        poststatus_distribution = [str(post_status.post_status) for post_status in records]

        poststatus_tally = Counter(poststatus_distribution)

        poststatus_frequency = poststatus_tally.most_common(1)[0][0]

    except:
        poststatus_frequency = ""

    try:
        poststatus_firstfrequency = poststatus_tally.most_common(1)[0][1]

        poststatus_firstlabel = poststatus_tally.most_common(1)[0][0] + " Frequency"

    except:
        poststatus_firstfrequency = ""
    
        poststatus_firstlabel = ""

    try:
        poststatus_secondfrequency = poststatus_tally.most_common(2)[1][1]

        poststatus_secondlabel = poststatus_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        poststatus_secondfrequency = ""
    
        poststatus_secondlabel = ""

    try:
        poststatus_thirdfrequency = poststatus_tally.most_common(3)[2][1] 

        poststatus_thirdlabel = poststatus_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        poststatus_thirdfrequency = ""
    
        poststatus_thirdlabel = ""

    try:
        size_distribution = [str(post_observation.post_observation.size) for post_observation in records]

        size_tally = Counter(size_distribution)

        size_frequency = size_tally.most_common(1)[0][0]

    except:
        size_frequency = ""
    
    try:
        size_firstfrequency = size_tally.most_common(1)[0][1]

        size_firstlabel = size_tally.most_common(1)[0][0] + " / Centimeter Frequency"

    except:
        size_firstfrequency = ""
    
        size_firstlabel = ""
    
    try:
        size_secondfrequency = size_tally.most_common(2)[1][1]

        size_secondlabel = size_tally.most_common(2)[1][0] + " / Centimeter Frequency"
    
    except:
        size_secondfrequency = ""
    
        size_secondlabel = ""
    
    try:
        size_thirdfrequency = size_tally.most_common(3)[2][1] 

        size_thirdlabel = size_tally.most_common(3)[2][0] + " / Centimeter Frequency"
    
    except:
        size_thirdfrequency = ""
    
        size_thirdlabel = ""

    try:
        density_distribution = [str(post_observation.post_observation.density) for post_observation in records]

        density_tally = Counter(density_distribution)

        density_frequency = density_tally.most_common(1)[0][0]
    
    except:
        density_frequency = ""
    
    try:
        density_firstfrequency = density_tally.most_common(1)[0][1]

        density_firstlabel = density_tally.most_common(1)[0][0] + " / Square Meter Frequency"

    except:
        density_firstfrequency = ""
    
        density_firstlabel = ""
    
    try:
        density_secondfrequency = density_tally.most_common(2)[1][1]

        density_secondlabel = density_tally.most_common(2)[1][0] + " / Square Meter Frequency"
    
    except:
        density_secondfrequency = ""
    
        density_secondlabel = ""
    
    try:
        density_thirdfrequency = density_tally.most_common(3)[2][1] 

        density_thirdlabel = density_tally.most_common(3)[2][0] + " / Square Meter Frequency"
    
    except:
        density_thirdfrequency = ""
    
        density_thirdlabel = ""

    try:
        depth_distribution = [str(post_observation.post_observation.depth) for post_observation in records]

        depth_tally = Counter(depth_distribution)

        depth_frequency = depth_tally.most_common(1)[0][0]
    
    except:
        depth_frequency = ""
    
    try:
        depth_firstfrequency = depth_tally.most_common(1)[0][1]

        depth_firstlabel = depth_tally.most_common(1)[0][0] + " Frequency"

    except:
        depth_firstfrequency = ""
    
        depth_firstlabel = ""
    
    try:
        depth_secondfrequency = depth_tally.most_common(2)[1][1]

        depth_secondlabel = depth_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        depth_secondfrequency = ""
    
        depth_secondlabel = ""
    
    try:
        depth_thirdfrequency = depth_tally.most_common(3)[2][1] 

        depth_thirdlabel = depth_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        depth_thirdfrequency = ""
    
        depth_thirdlabel = ""

    try:
        weather_distribution = [str(post_observation.post_observation.weather) for post_observation in records]

        weather_tally = Counter(weather_distribution)

        weather_frequency = weather_tally.most_common(1)[0][0]

    except:
        weather_frequency = ""
    
    try:
        weather_firstfrequency = weather_tally.most_common(1)[0][1]

        weather_firstlabel = weather_tally.most_common(1)[0][0] + " Frequency"

    except:
        weather_firstfrequency = ""
    
        weather_firstlabel = ""
    
    try:
        weather_secondfrequency = weather_tally.most_common(2)[1][1]

        weather_secondlabel = weather_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        weather_secondfrequency = ""
    
        weather_secondlabel = ""
    
    try:
        weather_thirdfrequency = weather_tally.most_common(3)[2][1] 

        weather_thirdlabel = weather_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        weather_thirdfrequency = ""
    
        weather_thirdlabel = ""

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        user = request.GET.get("user")

        post_status = request.GET.get("post_status")

        depth = request.GET.get("depth")

        weather = request.GET.get("weather")

        if from_date and to_date:
            results = Post.objects.filter(capture_date__range = [from_date, to_date])
        
        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 
        
        elif not from_date or not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 

        if user and not user == "each_user":
            results = Post.objects.filter(user = user)

        elif not user and user == "each_user":
            results = Post.objects.all()
        
        elif not user and not user == "each_user":
            username = request.user.username

            messages.error(request, username + ", " + "user is not valid.")
        
        elif not user or not user == "each_user":
            username = request.user.username

            messages.error(request, username + ", " + "user is not valid.") 

        if post_status and not post_status == "each_poststatus":
            results = Post.objects.filter(post_status = post_status)[:50]
    
        elif not post_status and post_status == "each_poststatus":
            results = Post.objects.all()[:50]

        elif not post_status and not post_status == "each_poststatus":
            username = request.user.username

            messages.error(request, username + ", " + "post status is not valid.")
        
        elif not post_status or not post_status == "each_poststatus":
            username = request.user.username

            messages.error(request, username + ", " + "post status is not valid.") 
        
        if depth and not depth == "each_depth":
            results = Post.objects.filter(post_observation__depth = depth)
    
        elif not depth and depth == "each_depth":
            results = Post.objects.all()

        elif not depth and not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")
        
        elif not depth or not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")

        if weather and not weather == "each_weather":
            results = Post.objects.filter(post_observation__weather = weather)
    
        elif not weather and weather == "each_weather":
            results = Post.objects.all()

        elif not weather and not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")
        
        elif not weather or not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")  

        if not from_date and not to_date and not user and not post_status and not depth and not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        elif not from_date or not to_date or not user or not post_status or not depth or not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")

        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter posts within COTSEye to generate for reports today.")
        
        elif results is not None:
            try:
                posts_count = results.count()

                posts_label = "Posts" + " Count"
    
            except:
                posts_count = ""

                posts_label = ""

            try:
                users_count = results.values("user").distinct().count()

                users_label = "Users" + " Count"
        
            except:
                users_count = ""

                users_label = ""

            try:
                user_distribution = [str(user.user) for user in results]

                user_tally = Counter(user_distribution)
                
                user_frequency = user_tally.most_common(1)[0][0]
            
            except:
                user_frequency = ""
            
            try:
                user_firstfrequency = user_tally.most_common(1)[0][1]

                user_firstlabel = user_tally.most_common(1)[0][0] + " Frequency"

            except:
                user_firstfrequency = ""
            
                user_firstlabel = ""
            
            try:
                user_secondfrequency = user_tally.most_common(2)[1][1]

                user_secondlabel = user_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                user_secondfrequency = ""
            
                user_secondlabel = ""
            
            try:
                user_thirdfrequency = size_tally.most_common(3)[2][1] 

                user_thirdlabel = size_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                user_thirdfrequency = ""
            
                user_thirdlabel = ""

            try:
                poststatus_distribution = [str(post_status.post_status) for post_status in results]

                poststatus_tally = Counter(poststatus_distribution)

                poststatus_frequency = poststatus_tally.most_common(1)[0][0]

            except:
                poststatus_frequency = ""

            try:
                poststatus_firstfrequency = poststatus_tally.most_common(1)[0][1]

                poststatus_firstlabel = poststatus_tally.most_common(1)[0][0] + " Frequency"

            except:
                poststatus_firstfrequency = ""
            
                poststatus_firstlabel = ""

            try:
                poststatus_secondfrequency = poststatus_tally.most_common(2)[1][1]

                poststatus_secondlabel = poststatus_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                poststatus_secondfrequency = ""
            
                poststatus_secondlabel = ""

            try:
                poststatus_thirdfrequency = poststatus_tally.most_common(3)[2][1] 

                poststatus_thirdlabel = poststatus_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                poststatus_thirdfrequency = ""
            
                poststatus_thirdlabel = ""

            try:
                size_distribution = [str(post_observation.post_observation.size) for post_observation in results]

                size_tally = Counter(size_distribution)

                size_frequency = size_tally.most_common(1)[0][0]

            except:
                size_frequency = ""
            
            try:
                size_firstfrequency = size_tally.most_common(1)[0][1]

                size_firstlabel = size_tally.most_common(1)[0][0] + " / Centimeter Frequency"

            except:
                size_firstfrequency = ""
            
                size_firstlabel = ""
            
            try:
                size_secondfrequency = size_tally.most_common(2)[1][1]

                size_secondlabel = size_tally.most_common(2)[1][0] + " / Centimeter Frequency"
            
            except:
                size_secondfrequency = ""
            
                size_secondlabel = ""
            
            try:
                size_thirdfrequency = size_tally.most_common(3)[2][1] 

                size_thirdlabel = size_tally.most_common(3)[2][0] + " / Centimeter Frequency"
            
            except:
                size_thirdfrequency = ""
            
                size_thirdlabel = ""

            try:
                density_distribution = [str(post_observation.post_observation.density) for post_observation in results]

                density_tally = Counter(density_distribution)

                density_frequency = density_tally.most_common(1)[0][0]
            
            except:
                density_frequency = ""
            
            try:
                density_firstfrequency = density_tally.most_common(1)[0][1]

                density_firstlabel = density_tally.most_common(1)[0][0] + " / Square Meter Frequency"

            except:
                density_firstfrequency = ""
            
                density_firstlabel = ""
            
            try:
                density_secondfrequency = density_tally.most_common(2)[1][1]

                density_secondlabel = density_tally.most_common(2)[1][0] + " / Square Meter Frequency"
            
            except:
                density_secondfrequency = ""
            
                density_secondlabel = ""
            
            try:
                density_thirdfrequency = density_tally.most_common(3)[2][1] 

                density_thirdlabel = density_tally.most_common(3)[2][0] + " / Square Meter Frequency"
            
            except:
                density_thirdfrequency = ""
            
                density_thirdlabel = ""

            try:
                depth_distribution = [str(post_observation.post_observation.depth) for post_observation in results]

                depth_tally = Counter(depth_distribution)

                depth_frequency = depth_tally.most_common(1)[0][0]
            
            except:
                depth_frequency = ""
            
            try:
                depth_firstfrequency = depth_tally.most_common(1)[0][1]

                depth_firstlabel = depth_tally.most_common(1)[0][0] + " Frequency"

            except:
                depth_firstfrequency = ""
            
                depth_firstlabel = ""
            
            try:
                depth_secondfrequency = depth_tally.most_common(2)[1][1]

                depth_secondlabel = depth_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                depth_secondfrequency = ""
            
                depth_secondlabel = ""
            
            try:
                depth_thirdfrequency = depth_tally.most_common(3)[2][1] 

                depth_thirdlabel = depth_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                depth_thirdfrequency = ""
            
                depth_thirdlabel = ""

            try:
                weather_distribution = [str(post_observation.post_observation.weather) for post_observation in results]

                weather_tally = Counter(weather_distribution)

                weather_frequency = weather_tally.most_common(1)[0][0]

            except:
                weather_frequency = ""
            
            try:
                weather_firstfrequency = weather_tally.most_common(1)[0][1]

                weather_firstlabel = weather_tally.most_common(1)[0][0] + " Frequency"

            except:
                weather_firstfrequency = ""
            
                weather_firstlabel = ""
            
            try:
                weather_secondfrequency = weather_tally.most_common(2)[1][1]

                weather_secondlabel = weather_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                weather_secondfrequency = ""
            
                weather_secondlabel = ""
            
            try:
                weather_thirdfrequency = weather_tally.most_common(3)[2][1] 

                weather_thirdlabel = weather_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                weather_thirdfrequency = ""
            
                weather_thirdlabel = ""

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "options": options, "records": records, "results": results, "posts_count": posts_count, "posts_label": posts_label, "users_count": users_count, "users_label": users_label, "user_frequency": user_frequency, "user_firstfrequency": user_firstfrequency, "user_firstlabel": user_firstlabel, "user_secondfrequency": user_secondfrequency, "user_secondlabel": user_secondlabel, "user_thirdfrequency": user_thirdfrequency, "user_thirdlabel": user_thirdlabel, "poststatus_frequency": poststatus_frequency, "poststatus_firstfrequency": poststatus_firstfrequency, "poststatus_firstlabel": poststatus_firstlabel, "poststatus_secondfrequency": poststatus_secondfrequency, "poststatus_secondlabel": poststatus_secondlabel, "poststatus_thirdfrequency": poststatus_thirdfrequency, "poststatus_thirdlabel": poststatus_thirdlabel, "size_frequency": size_frequency, "size_firstfrequency": size_firstfrequency, "size_firstlabel": size_firstlabel, "size_secondfrequency": size_secondfrequency, "size_secondlabel": size_secondlabel, "size_thirdfrequency": size_thirdfrequency, "size_thirdlabel": size_thirdlabel, "density_frequency": density_frequency, "density_firstfrequency": density_firstfrequency, "density_firstlabel": density_firstlabel, "density_secondfrequency": density_secondfrequency, "density_secondlabel": density_secondlabel, "density_thirdfrequency": density_thirdfrequency, "density_thirdlabel": density_thirdlabel, "depth_frequency": depth_frequency, "depth_firstfrequency": depth_firstfrequency, "depth_firstlabel": depth_firstlabel, "depth_secondfrequency": depth_secondfrequency, "depth_secondlabel": depth_secondlabel, "depth_thirdfrequency": depth_thirdfrequency, "depth_thirdlabel": depth_thirdlabel, "weather_frequency": weather_frequency, "weather_firstfrequency": weather_firstfrequency, "weather_firstlabel": weather_firstlabel, "weather_secondfrequency": weather_secondfrequency, "weather_secondlabel": weather_secondlabel, "weather_thirdfrequency": weather_thirdfrequency, "weather_thirdlabel": weather_thirdlabel}

    return render(request, "officer/control/post/post.html", context)


@login_required(login_url = "admin:Administrator Control Login")
@user_passes_test(AdministratorCheck, login_url = "admin:Administrator Control Login")
def AdministratorControlStatisticsPost(request):
    username = request.user.username

    options = Post.objects.all()

    records = Post.objects.all()

    results = None

    try:
        posts_count = records.count()

        posts_label = "Posts" + " Count"
    
    except:
        posts_count = ""

        posts_label = ""

    try:
        users_count = records.values("user").distinct().count()

        users_label = "Users" + " Count"
    
    except:
        users_count = ""

        users_label = ""

    try:
        user_distribution = [str(user.user) for user in records]

        user_tally = Counter(user_distribution)
        
        user_frequency = user_tally.most_common(1)[0][0]
    
    except:
        user_frequency = ""
    
    try:
        user_firstfrequency = user_tally.most_common(1)[0][1]

        user_firstlabel = user_tally.most_common(1)[0][0] + " Frequency"

    except:
        user_firstfrequency = ""
    
        user_firstlabel = ""
    
    try:
        user_secondfrequency = user_tally.most_common(2)[1][1]

        user_secondlabel = user_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        user_secondfrequency = ""
    
        user_secondlabel = ""
    
    try:
        user_thirdfrequency = size_tally.most_common(3)[2][1] 

        user_thirdlabel = size_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        user_thirdfrequency = ""
    
        user_thirdlabel = ""

    try:
        poststatus_distribution = [str(post_status.post_status) for post_status in records]

        poststatus_tally = Counter(poststatus_distribution)

        poststatus_frequency = poststatus_tally.most_common(1)[0][0]

    except:
        poststatus_frequency = ""

    try:
        poststatus_firstfrequency = poststatus_tally.most_common(1)[0][1]

        poststatus_firstlabel = poststatus_tally.most_common(1)[0][0] + " Frequency"

    except:
        poststatus_firstfrequency = ""
    
        poststatus_firstlabel = ""

    try:
        poststatus_secondfrequency = poststatus_tally.most_common(2)[1][1]

        poststatus_secondlabel = poststatus_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        poststatus_secondfrequency = ""
    
        poststatus_secondlabel = ""

    try:
        poststatus_thirdfrequency = poststatus_tally.most_common(3)[2][1] 

        poststatus_thirdlabel = poststatus_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        poststatus_thirdfrequency = ""
    
        poststatus_thirdlabel = ""

    try:
        size_distribution = [str(post_observation.post_observation.size) for post_observation in records]

        size_tally = Counter(size_distribution)

        size_frequency = size_tally.most_common(1)[0][0]

    except:
        size_frequency = ""
    
    try:
        size_firstfrequency = size_tally.most_common(1)[0][1]

        size_firstlabel = size_tally.most_common(1)[0][0] + " / Centimeter Frequency"

    except:
        size_firstfrequency = ""
    
        size_firstlabel = ""
    
    try:
        size_secondfrequency = size_tally.most_common(2)[1][1]

        size_secondlabel = size_tally.most_common(2)[1][0] + " / Centimeter Frequency"
    
    except:
        size_secondfrequency = ""
    
        size_secondlabel = ""
    
    try:
        size_thirdfrequency = size_tally.most_common(3)[2][1] 

        size_thirdlabel = size_tally.most_common(3)[2][0] + " / Centimeter Frequency"
    
    except:
        size_thirdfrequency = ""
    
        size_thirdlabel = ""

    try:
        density_distribution = [str(post_observation.post_observation.density) for post_observation in records]

        density_tally = Counter(density_distribution)

        density_frequency = density_tally.most_common(1)[0][0]
    
    except:
        density_frequency = ""
    
    try:
        density_firstfrequency = density_tally.most_common(1)[0][1]

        density_firstlabel = density_tally.most_common(1)[0][0] + " / Square Meter Frequency"

    except:
        density_firstfrequency = ""
    
        density_firstlabel = ""
    
    try:
        density_secondfrequency = density_tally.most_common(2)[1][1]

        density_secondlabel = density_tally.most_common(2)[1][0] + " / Square Meter Frequency"
    
    except:
        density_secondfrequency = ""
    
        density_secondlabel = ""
    
    try:
        density_thirdfrequency = density_tally.most_common(3)[2][1] 

        density_thirdlabel = density_tally.most_common(3)[2][0] + " / Square Meter Frequency"
    
    except:
        density_thirdfrequency = ""
    
        density_thirdlabel = ""

    try:
        depth_distribution = [str(post_observation.post_observation.depth) for post_observation in records]

        depth_tally = Counter(depth_distribution)

        depth_frequency = depth_tally.most_common(1)[0][0]
    
    except:
        depth_frequency = ""
    
    try:
        depth_firstfrequency = depth_tally.most_common(1)[0][1]

        depth_firstlabel = depth_tally.most_common(1)[0][0] + " Frequency"

    except:
        depth_firstfrequency = ""
    
        depth_firstlabel = ""
    
    try:
        depth_secondfrequency = depth_tally.most_common(2)[1][1]

        depth_secondlabel = depth_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        depth_secondfrequency = ""
    
        depth_secondlabel = ""
    
    try:
        depth_thirdfrequency = depth_tally.most_common(3)[2][1] 

        depth_thirdlabel = depth_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        depth_thirdfrequency = ""
    
        depth_thirdlabel = ""

    try:
        weather_distribution = [str(post_observation.post_observation.weather) for post_observation in records]

        weather_tally = Counter(weather_distribution)

        weather_frequency = weather_tally.most_common(1)[0][0]

    except:
        weather_frequency = ""
    
    try:
        weather_firstfrequency = weather_tally.most_common(1)[0][1]

        weather_firstlabel = weather_tally.most_common(1)[0][0] + " Frequency"

    except:
        weather_firstfrequency = ""
    
        weather_firstlabel = ""
    
    try:
        weather_secondfrequency = weather_tally.most_common(2)[1][1]

        weather_secondlabel = weather_tally.most_common(2)[1][0] + " Frequency"
    
    except:
        weather_secondfrequency = ""
    
        weather_secondlabel = ""
    
    try:
        weather_thirdfrequency = weather_tally.most_common(3)[2][1] 

        weather_thirdlabel = weather_tally.most_common(3)[2][0] + " Frequency"
    
    except:
        weather_thirdfrequency = ""
    
        weather_thirdlabel = ""

    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
        
        to_date = request.GET.get("to_date")

        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

        user = request.GET.get("user")

        post_status = request.GET.get("post_status")

        depth = request.GET.get("depth")

        weather = request.GET.get("weather")

        if from_date and to_date:
            results = Post.objects.filter(capture_date__range = [from_date, to_date])
        
        elif from_date and to_date and to_date < from_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.")

        elif not from_date and not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 
        
        elif not from_date or not to_date:
            username = request.user.username

            messages.error(request, username + ", " + "date range is not valid.") 

        if user and not user == "each_user":
            results = Post.objects.filter(user = user)

        elif not user and user == "each_user":
            results = Post.objects.all()
        
        elif not user and not user == "each_user":
            username = request.user.username

            messages.error(request, username + ", " + "user is not valid.")
        
        elif not user or not user == "each_user":
            username = request.user.username

            messages.error(request, username + ", " + "user is not valid.") 

        if post_status and not post_status == "each_poststatus":
            results = Post.objects.filter(post_status = post_status)[:50]
    
        elif not post_status and post_status == "each_poststatus":
            results = Post.objects.all()[:50]

        elif not post_status and not post_status == "each_poststatus":
            username = request.user.username

            messages.error(request, username + ", " + "post status is not valid.")
        
        elif not post_status or not post_status == "each_poststatus":
            username = request.user.username

            messages.error(request, username + ", " + "post status is not valid.") 
        
        if depth and not depth == "each_depth":
            results = Post.objects.filter(post_observation__depth = depth)
    
        elif not depth and depth == "each_depth":
            results = Post.objects.all()

        elif not depth and not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")
        
        elif not depth or not depth == "each_depth":
            username = request.user.username

            messages.error(request, username + ", " + "depth is not valid.")

        if weather and not weather == "each_weather":
            results = Post.objects.filter(post_observation__weather = weather)
    
        elif not weather and weather == "each_weather":
            results = Post.objects.all()

        elif not weather and not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")
        
        elif not weather or not weather == "each_weather":
            username = request.user.username

            messages.error(request, username + ", " + "weather is not valid.")  

        if not from_date and not to_date and not user and not post_status and not depth and not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is empty within COTSEye.")
        
        elif not from_date or not to_date or not user or not post_status or not depth or not weather:
            username = request.user.username

            messages.error(request, username + ", " + "information filter is incomplete within COTSEye.")

        if results is None:
            username = request.user.username

            messages.info(request, username + ", " + "kindly filter posts within COTSEye to generate for reports today.")
        
        elif results is not None:
            try:
                posts_count = results.count()

                posts_label = "Posts" + " Count"
    
            except:
                posts_count = ""

                posts_label = ""

            try:
                users_count = results.values("user").distinct().count()

                users_label = "Users" + " Count"
        
            except:
                users_count = ""

                users_label = ""

            try:
                user_distribution = [str(user.user) for user in results]

                user_tally = Counter(user_distribution)
                
                user_frequency = user_tally.most_common(1)[0][0]
            
            except:
                user_frequency = ""
            
            try:
                user_firstfrequency = user_tally.most_common(1)[0][1]

                user_firstlabel = user_tally.most_common(1)[0][0] + " Frequency"

            except:
                user_firstfrequency = ""
            
                user_firstlabel = ""
            
            try:
                user_secondfrequency = user_tally.most_common(2)[1][1]

                user_secondlabel = user_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                user_secondfrequency = ""
            
                user_secondlabel = ""
            
            try:
                user_thirdfrequency = size_tally.most_common(3)[2][1] 

                user_thirdlabel = size_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                user_thirdfrequency = ""
            
                user_thirdlabel = ""

            try:
                poststatus_distribution = [str(post_status.post_status) for post_status in results]

                poststatus_tally = Counter(poststatus_distribution)

                poststatus_frequency = poststatus_tally.most_common(1)[0][0]

            except:
                poststatus_frequency = ""

            try:
                poststatus_firstfrequency = poststatus_tally.most_common(1)[0][1]

                poststatus_firstlabel = poststatus_tally.most_common(1)[0][0] + " Frequency"

            except:
                poststatus_firstfrequency = ""
            
                poststatus_firstlabel = ""

            try:
                poststatus_secondfrequency = poststatus_tally.most_common(2)[1][1]

                poststatus_secondlabel = poststatus_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                poststatus_secondfrequency = ""
            
                poststatus_secondlabel = ""

            try:
                poststatus_thirdfrequency = poststatus_tally.most_common(3)[2][1] 

                poststatus_thirdlabel = poststatus_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                poststatus_thirdfrequency = ""
            
                poststatus_thirdlabel = ""

            try:
                size_distribution = [str(post_observation.post_observation.size) for post_observation in results]

                size_tally = Counter(size_distribution)

                size_frequency = size_tally.most_common(1)[0][0]

            except:
                size_frequency = ""
            
            try:
                size_firstfrequency = size_tally.most_common(1)[0][1]

                size_firstlabel = size_tally.most_common(1)[0][0] + " / Centimeter Frequency"

            except:
                size_firstfrequency = ""
            
                size_firstlabel = ""
            
            try:
                size_secondfrequency = size_tally.most_common(2)[1][1]

                size_secondlabel = size_tally.most_common(2)[1][0] + " / Centimeter Frequency"
            
            except:
                size_secondfrequency = ""
            
                size_secondlabel = ""
            
            try:
                size_thirdfrequency = size_tally.most_common(3)[2][1] 

                size_thirdlabel = size_tally.most_common(3)[2][0] + " / Centimeter Frequency"
            
            except:
                size_thirdfrequency = ""
            
                size_thirdlabel = ""

            try:
                density_distribution = [str(post_observation.post_observation.density) for post_observation in results]

                density_tally = Counter(density_distribution)

                density_frequency = density_tally.most_common(1)[0][0]
            
            except:
                density_frequency = ""
            
            try:
                density_firstfrequency = density_tally.most_common(1)[0][1]

                density_firstlabel = density_tally.most_common(1)[0][0] + " / Square Meter Frequency"

            except:
                density_firstfrequency = ""
            
                density_firstlabel = ""
            
            try:
                density_secondfrequency = density_tally.most_common(2)[1][1]

                density_secondlabel = density_tally.most_common(2)[1][0] + " / Square Meter Frequency"
            
            except:
                density_secondfrequency = ""
            
                density_secondlabel = ""
            
            try:
                density_thirdfrequency = density_tally.most_common(3)[2][1] 

                density_thirdlabel = density_tally.most_common(3)[2][0] + " / Square Meter Frequency"
            
            except:
                density_thirdfrequency = ""
            
                density_thirdlabel = ""

            try:
                depth_distribution = [str(post_observation.post_observation.depth) for post_observation in results]

                depth_tally = Counter(depth_distribution)

                depth_frequency = depth_tally.most_common(1)[0][0]
            
            except:
                depth_frequency = ""
            
            try:
                depth_firstfrequency = depth_tally.most_common(1)[0][1]

                depth_firstlabel = depth_tally.most_common(1)[0][0] + " Frequency"

            except:
                depth_firstfrequency = ""
            
                depth_firstlabel = ""
            
            try:
                depth_secondfrequency = depth_tally.most_common(2)[1][1]

                depth_secondlabel = depth_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                depth_secondfrequency = ""
            
                depth_secondlabel = ""
            
            try:
                depth_thirdfrequency = depth_tally.most_common(3)[2][1] 

                depth_thirdlabel = depth_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                depth_thirdfrequency = ""
            
                depth_thirdlabel = ""

            try:
                weather_distribution = [str(post_observation.post_observation.weather) for post_observation in results]

                weather_tally = Counter(weather_distribution)

                weather_frequency = weather_tally.most_common(1)[0][0]

            except:
                weather_frequency = ""
            
            try:
                weather_firstfrequency = weather_tally.most_common(1)[0][1]

                weather_firstlabel = weather_tally.most_common(1)[0][0] + " Frequency"

            except:
                weather_firstfrequency = ""
            
                weather_firstlabel = ""
            
            try:
                weather_secondfrequency = weather_tally.most_common(2)[1][1]

                weather_secondlabel = weather_tally.most_common(2)[1][0] + " Frequency"
            
            except:
                weather_secondfrequency = ""
            
                weather_secondlabel = ""
            
            try:
                weather_thirdfrequency = weather_tally.most_common(3)[2][1] 

                weather_thirdlabel = weather_tally.most_common(3)[2][0] + " Frequency"
            
            except:
                weather_thirdfrequency = ""
            
                weather_thirdlabel = ""

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")

    context = {"username": username, "options": options, "records": records, "results": results, "posts_count": posts_count, "posts_label": posts_label, "users_count": users_count, "users_label": users_label, "user_frequency": user_frequency, "user_firstfrequency": user_firstfrequency, "user_firstlabel": user_firstlabel, "user_secondfrequency": user_secondfrequency, "user_secondlabel": user_secondlabel, "user_thirdfrequency": user_thirdfrequency, "user_thirdlabel": user_thirdlabel, "poststatus_frequency": poststatus_frequency, "poststatus_firstfrequency": poststatus_firstfrequency, "poststatus_firstlabel": poststatus_firstlabel, "poststatus_secondfrequency": poststatus_secondfrequency, "poststatus_secondlabel": poststatus_secondlabel, "poststatus_thirdfrequency": poststatus_thirdfrequency, "poststatus_thirdlabel": poststatus_thirdlabel, "size_frequency": size_frequency, "size_firstfrequency": size_firstfrequency, "size_firstlabel": size_firstlabel, "size_secondfrequency": size_secondfrequency, "size_secondlabel": size_secondlabel, "size_thirdfrequency": size_thirdfrequency, "size_thirdlabel": size_thirdlabel, "density_frequency": density_frequency, "density_firstfrequency": density_firstfrequency, "density_firstlabel": density_firstlabel, "density_secondfrequency": density_secondfrequency, "density_secondlabel": density_secondlabel, "density_thirdfrequency": density_thirdfrequency, "density_thirdlabel": density_thirdlabel, "depth_frequency": depth_frequency, "depth_firstfrequency": depth_firstfrequency, "depth_firstlabel": depth_firstlabel, "depth_secondfrequency": depth_secondfrequency, "depth_secondlabel": depth_secondlabel, "depth_thirdfrequency": depth_thirdfrequency, "depth_thirdlabel": depth_thirdlabel, "weather_frequency": weather_frequency, "weather_firstfrequency": weather_firstfrequency, "weather_firstlabel": weather_firstlabel, "weather_secondfrequency": weather_secondfrequency, "weather_secondlabel": weather_secondlabel, "weather_thirdfrequency": weather_thirdfrequency, "weather_thirdlabel": weather_thirdlabel}

    return render(request, "admin/control/post/post.html", context)


def PostValidReadRedirect(request):
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            object = Post.objects.get()

            return redirect(reverse("Contributor Service Post Valid Read", kwargs = {"id": object.id}))

        elif usertype == 2:
            object = Account.objects.get(id = request.user.id)

            return redirect(reverse("officer:reports_post_change", kwargs = {"object_id": object.id}))

        elif usertype == 1:
            object = Account.objects.get(id = request.user.id)

            return redirect(reverse("admin:reports_post_change", kwargs = {"object_id": object.id}))
    
    else:
        object = Post.objects.get()

        return redirect(reverse("Public Service Post Valid Read", kwargs = {"id": object.id}))


def ControlStatisticsPostReadRedirect(request, object_id):
    object = Post.objects.get(id = object_id)

    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            return redirect(reverse("officer:reports_post_change", kwargs = {"object_id": object.id}))
        
        elif usertype == 2:
            return redirect(reverse("officer:reports_post_change", kwargs = {"object_id": object.id}))

        elif usertype == 1:
            return redirect(reverse("admin:reports_post_change", kwargs = {"object_id": object.id}))

    else:
        return redirect(reverse("officer:reports_post_change", kwargs = {"object_id": object.id}))     