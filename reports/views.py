from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from authentications.models import Account, Notification
from authentications.views import ContributorCheck, CuratorCheck
from managements.models import Location, Municipality, Barangay
from reports.models import *
from reports.forms import CoordinatesForm, PostObservationForm, PostForm
from datetime import timedelta
from django.db.models import Case, When, IntegerField
from django.core.files.storage import default_storage
from django.http import HttpResponseNotFound, HttpResponse, Http404

import base64
import json


# Create your views here.
def PublicServicePostFeed(request):
    username = "public/everyone"

    valid_posts = Post.objects.filter(post_status = 1).order_by("-creation_date")

    context = {"username": username, "valid_posts": valid_posts}
    
    return render(request, "public/service/post/feed.html", context)


def PublicServicePostFeedRead(request, id):
    username = "public/everyone"

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    valid_post = Post.objects.get(id = id, post_status = 1)
    
    context = {"username": username, "scheme": scheme, "host": host, "valid_post": valid_post}
    
    return render(request, "public/service/post/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceReport(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    locations = Location.objects.all()

    municipalities = Municipality.objects.values("municipality_name").distinct()

    coordinates_form = CoordinatesForm()

    postobservation_form = PostObservationForm()

    sizes = Size.objects.all()

    depths = Depth.objects.all()

    densities = Density.objects.all()

    post_form = PostForm()

    selected_density = None

    density = request.POST.get("density")
    
    if density is not None and density != "":
        selected_density = Density.objects.get(id = density)

    selected_size = None

    size = request.POST.get("size")

    if size is not None and size != "":
        selected_size = Size.objects.get(id = size)

    selected_depth = None

    depth = request.POST.get("depth")

    if depth is not None and depth != "":
        selected_depth = Depth.objects.get(id = depth)

    selected_longitude = 125.1929

    selected_latitude = 5.9656

    selected_municipality = None

    selected_barangay = None

    barangay = request.POST.get("barangay")

    municipality = request.POST.get("municipality")

    try:
        if barangay and barangay.strip():
            if barangay.isdigit():
                location = get_object_or_404(Location, id = barangay)
            else:
                location = get_object_or_404(Location, barangay__barangay_name = barangay)

            selected_barangay = Barangay.objects.get(id = location.barangay.id)

        if municipality and municipality.strip():
            if municipality.isdigit():
                location = get_object_or_404(Location, municipality = municipality, barangay = selected_barangay)

            else:
                location = get_object_or_404(Location, municipality__municipality_name = municipality, barangay = selected_barangay)

            selected_municipality = Municipality.objects.get(id = location.municipality.id)

    except Http404 as error:
        messages.error(request, f"There is an error: {error}. Kindly check the barangay and municipality input again.")

    selected_longitude = request.POST.get("longitude")

    if selected_longitude is not None and selected_longitude != "":
        longitude = request.POST.get("longitude")

        selected_longitude = longitude

    else:
        selected_longitude = 125.1929

    selected_latitude = request.POST.get("latitude")

    if selected_latitude is not None and selected_latitude != "":
        latitude = request.POST.get("latitude")
        
        selected_latitude = latitude

    else:
        selected_latitude = 5.9656
     
    location_data = {
        "selected_latitude": selected_latitude,

        "selected_longitude": selected_longitude
    }

    location_data_json = json.dumps(location_data)

    post_photos_capture = request.FILES.getlist("post_photos_capture")

    post_photos_choose = request.FILES.getlist("post_photos_choose")

    post_photos = post_photos_capture + post_photos_choose

    if post_photos is not None:
        photo_urls = [default_storage.url(photo.name).replace("/assets/", "/assets/posts/") for photo in post_photos]

    else:
        photo_urls = []

    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST)

        postobservation_form = PostObservationForm(request.POST)

        post_form =  PostForm(request.POST, request.FILES)

        if coordinates_form.is_valid() and postobservation_form.is_valid() and post_form.is_valid():
            coordinates = coordinates_form.save(commit = False)

            post_observation = postobservation_form.save(commit = False)

            post = post_form.save(commit = False)

            barangay = request.POST.get("barangay")

            try:
                selected_barangay = Location.objects.get(barangay = barangay)

            except:
                selected_barangay = None

            selected_longitude = request.POST.get("longitude")

            selected_latitude = request.POST.get("latitude")

            user = request.user.user

            action = request.POST.get("action")

            if action == "save and submit":
                post_status = PostStatus.objects.get(id = 3)

            elif action == "save as draft":
                post_status = PostStatus.objects.get(id = 4)

            coordinates = Coordinates.objects.create(latitude = coordinates.latitude, longitude = coordinates.longitude)
            
            size = request.POST.get("size")

            try:
                selected_size = Size.objects.get(id = size)

                post_observation.size = Size.objects.get(id = size)

            except:
                post_observation.size = None

            depth = request.POST.get("depth")

            try:
                selected_depth = Depth.objects.get(id = depth)

                post_observation.depth = Depth.objects.get(id = depth)

            except:
                post_observation.depth = None

            density = request.POST.get("density")
           
            try:
                selected_density = Density.objects.get(id = density)
                
                post_observation.density = selected_density

            except:
                post_observation.density = None

            location = request.POST.get("barangay")

            try:
                if location is not None and location != "":
                    if location.isdigit():
                        location = get_object_or_404(Location, barangay = location)

                        post.location = Location.objects.get(id = location.id)

                    else:
                        location = get_object_or_404(Location, barangay__barangay_name = location)

                        post.location = Location.objects.get(id = location.id)

            except:
                messages.error(request, "There is an issue in the location field. This field is required.")

                context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "locations": locations, "municipalities": municipalities, "coordinates_form": coordinates_form, "sizes": sizes, "depths": depths, "postobservation_form": postobservation_form, "post_form": post_form}

                return render(request, "contributor/service/report/report.html", context)

            post_observation = PostObservation.objects.create(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather)
            
            if Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and PostObservation.objects.filter(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather).exists():
                six_hours_ago = timezone.now() - timedelta(hours = 6)

                recent_posts = Post.objects.filter(user = user, creation_date__gte = six_hours_ago)
                
                if recent_posts.exists() and action == "save and submit":
                    messages.error(request, username + ", " +  "you have already created a post within the last 6 hours.")
                
                    return redirect("Contributor Service Post")
                
                else:
                    post = Post.objects.create(user = user, description = post.description, capture_date = post.capture_date, coordinates = coordinates, location = post.location, post_status = post_status, post_observation = post_observation)
 
                    post_photos_capture = request.FILES.getlist("post_photos_capture")

                    post_photos_choose = request.FILES.getlist("post_photos_choose")

                    post_photos = post_photos_capture + post_photos_choose


                    for post_photo in post_photos:
                        photo = PostPhoto.objects.create(post_photo = post_photo)
                        
                        post.post_photos.add(photo)

                    username = request.user.username
                    
                    if post_status.id == 3:
                        messages.success(request, username + ", " + "your report has been successfully sent. Kindly wait for an approval email in the next 3 to 5 business days.")
                    
                    elif post_status.id == 4:
                        messages.success(request, username + ", " + "your report has been successfully saved. Kindly proceed to drafts to see changes.")

                    return redirect("Contributor Service Post")

        else:
            for field, errors in coordinates_form.errors.items():
                messages.error(request, "There is an issue in the" + " " + field + " field." + " " + ", ".join(errors))

            for field, errors in postobservation_form.errors.items():
                messages.error(request, "There is an issue in the" + " " + field + " field." + " " + ", ".join(errors))

            for field, errors in post_form.errors.items():
                messages.error(request, "There is an issue in the" + " " + field + " field." + " " + ", ".join(errors))

    else:
        coordinates_form = CoordinatesForm()
        
        postobservation_form = PostObservationForm()
        
        post_form = PostForm() 

    context = { 'photo_urls': photo_urls, 'selected_municipality':selected_municipality, 'location_data_json': location_data_json, 'selected_latitude': selected_latitude, 'selected_longitude': selected_longitude,'selected_barangay':selected_barangay, 'selected_depth': selected_depth, 'selected_size':selected_size,'selected_density': selected_density,"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "locations": locations, "municipalities": municipalities, "coordinates_form": coordinates_form, "sizes": sizes, "depths": depths, "densities": densities, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/service/report/report.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceReportFetch(request):
    if request.method == "POST":
        information = json.loads(request.body)

        for information in information:
            user = information.get("user")

            user = User.objects.get(account = user)

            capture_date = information.get("capture_date")

            description = information.get("description")

            post_photos = information.get("post_photos", [])

            latitude = information.get("latitude")

            longitude = information.get("longitude")

            location = information.get("location")

            size = information.get("size")

            depth = information.get("depth")

            density = information.get("density")

            weather = information.get("weather")

            action = information.get("action")
                
            if action == "save and submit":
                post_status = PostStatus.objects.get(id = 3)

            else:
                post_status = PostStatus.objects.get(id = 4)

            depth = Depth.objects.get(id = depth) if depth else None

            location = Location.objects.get(id = location) if location else None
                    
            coordinates = Coordinates.objects.create(latitude = latitude, longitude = longitude)

            post_observation = PostObservation.objects.create(size = size, depth = depth, density = density, weather = weather)

            post = Post.objects.create(user = user, capture_date = capture_date, description = description, coordinates = coordinates, location = location, post_status = post_status, post_observation = post_observation)

            for post_photo in post_photos:
                format, string = post_photo.split(";base64,")

                extension = format.split("/")[-1]

                post_photo = ContentFile(base64.b64decode(string), name = "POST " + str(post.id) + "." + extension)

                photo = PostPhoto.objects.create(post_photo = post_photo)
                    
                post.post_photos.add(photo)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePost(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    records = None

    results = None

    if request.method == "GET":
        post_status = request.GET.get("post_status")

        if post_status in ["1", "2", "3", "4"]:
            results = Post.objects.filter(user = request.user.user, post_status = post_status).order_by("-creation_date")

        else:
            results = Post.objects.filter(user = request.user.user).order_by("-creation_date")
        
    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "records": records, "results": results, "post_status": post_status}

    return render(request, "contributor/service/post/post.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostRead(request, id):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    try:
        valid_post = Post.objects.get(id = id, user = request.user.user, post_status = 1)
    
    except:
        valid_post = None

    try:
        invalid_post = Post.objects.get(id = id, user = request.user.user, post_status = 2)
    
    except:
        invalid_post = None

    try:
        pending_post = Post.objects.get(id = id, user = request.user.user, post_status = 3)
    
    except:
        pending_post = None

    try:
        draft_post = Post.objects.get(id = id, user = request.user.user, post_status = 4)
    
    except:
        draft_post = None
    
    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "scheme": scheme, "host": host, "valid_post": valid_post, "invalid_post": invalid_post, "pending_post": pending_post, "draft_post": draft_post}
    
    return render(request, "contributor/service/post/read.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostFeed(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    valid_posts = Post.objects.filter(post_status = 1).order_by("-creation_date")

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "valid_posts": valid_posts}
    
    return render(request, "contributor/service/post/feed.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostFeedRead(request, id):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days=30)

    user = User.objects.get(account=request.user)
    unread_notifications = Notification.objects.filter(user=user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    scheme = request.scheme

    host = request.META["HTTP_HOST"]

    valid_post = Post.objects.get(id = id, post_status = 1)
    
    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "scheme": scheme, "host": host, "valid_post": valid_post}
    
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
def ContributorServicePostInvalidDeleteFetch(request):
    if request.method == "POST":
        post = json.loads(request.body)

        for information in post:            
            post = Post.objects.get(id = information.get("id"), user = information.get("user"))

            post.coordinates.delete()

            post.post_observation.delete()

            for post_photo in post.post_photos.all():
                post.post_photos.remove(post_photo)

                post_photo.delete()
            
            post.delete()


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostDraftUpdate(request, id):
    username = request.user.username

    user_profile = get_object_or_404(User, account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    draft_post = get_object_or_404(Post, id = id, post_status = 4)

    locations = Location.objects.all()

    municipalities = Municipality.objects.values("municipality_name").distinct()

    selected_barangay = None
    barangay = request.POST.get("barangay")
    if barangay is not None and barangay != "":
        if barangay.isdigit():
            location = get_object_or_404(Location, barangay = barangay)

            selected_barangay = location.id

        else:
            location = get_object_or_404(Location, barangay__barangay_name = barangay)

            selected_barangay = location.id

    selected_longitude = request.POST.get("longitude")

    if selected_longitude is not None:
        longitude = request.POST.get("longitude")

        selected_longitude = longitude

    selected_latitude = request.POST.get("latitude")

    if selected_latitude is not None:
        latitude = request.POST.get("latitude")
        
        selected_latitude = latitude
    
    location_data = {
        "selected_latitude": selected_latitude,

        "selected_longitude": selected_longitude
    }

    location_data_json = json.dumps(location_data)


    if draft_post.location and draft_post.location.municipality:
        municipalities = municipalities.exclude(municipality_name = draft_post.location.municipality.municipality_name)

    sizes = Size.objects.all()

    depths = Depth.objects.all()

    densities = Density.objects.all()

    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST, instance = draft_post.coordinates)

        postobservation_form = PostObservationForm(request.POST, instance = draft_post.post_observation)

        post_form = PostForm(request.POST, request.FILES, instance = draft_post)

        if coordinates_form.is_valid() and postobservation_form.is_valid() and post_form.is_valid():
            coordinates_form.save()

            postobservation_form.save()

            post = post_form.save(commit = False)
            
            location = request.POST.get("barangay")

            try:
                post.location = Location.objects.get(id = location)

            except Location.DoesNotExist:
                post.location = None

            action = request.POST.get("action")

            if action == "save and submit":
                post_status = PostStatus.objects.get(id = 3)

            elif action == "save as draft":
                post_status = PostStatus.objects.get(id = 4)

            draft_post.post_status = post_status

            
            post.save()

            post_photos_capture = request.FILES.getlist("post_photos_capture")

            post_photos_choose = request.FILES.getlist("post_photos_choose")

            post_photos = post_photos_capture + post_photos_choose

            if post_photos:
                draft_post.post_photos.all().delete()

                for post_photo in post_photos:
                    photo = PostPhoto.objects.create(post_photo = post_photo)

                    draft_post.post_photos.add(photo)

            messages.success(request, username + ", " + "Your post has been successfully saved. Kindly proceed to drafts to see changes.")

            return redirect("Contributor Service Post")
        else:
            messages.error(request, "Information input is not valid.")

            messages.error(request, coordinates_form.errors)

            messages.error(request, postobservation_form.errors)

            messages.error(request, post_form.errors)

    else:
        coordinates_form = CoordinatesForm(instance = draft_post.coordinates)

        postobservation_form = PostObservationForm(instance = draft_post.post_observation)

        post_form = PostForm(instance = draft_post)

    context = {'selected_barangay': selected_barangay,  'location_data_json': location_data_json, 'selected_latitude': selected_latitude, 'selected_longitude': selected_longitude, "username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "draft_post": draft_post, "locations": locations, "municipalities": municipalities, "coordinates_form": coordinates_form, "sizes": sizes, "depths": depths, "densities": densities, "postobservation_form": postobservation_form, "post_form": post_form}

    return render(request, "contributor/service/report/report.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostDraftUpdateFetch(request):
    if request.method == "POST":
        information = json.loads(request.body)

        for information in information:
            id = information.get("id")

            user = information.get("user")

            user = User.objects.get(account = user)

            capture_date = information.get("capture_date")

            description = information.get("description")

            post_photos = information.get("post_photos", [])

            latitude = information.get("latitude")
            
            longitude = information.get("longitude")

            location = information.get("location")
            
            size = information.get("size")
            
            depth = information.get("depth")
            
            density = information.get("density")
            
            weather = information.get("weather")

            coordinates = Coordinates.objects.create(latitude = latitude, longitude = longitude)

            depth = Depth.objects.get(id = depth) if depth else None

            location = Location.objects.get(id = location) if location else None

            post_observation = PostObservation.objects.create(size = size, depth = depth, density = density, weather = weather)
            
            post = Post.objects.get(id = id, user = user)

            post.capture_date = capture_date

            post.description = description

            post.coordinates.delete()

            post.coordinates = coordinates

            post.location = location

            post.post_observation.delete()

            post.post_observation = post_observation
            
            coordinates.save()

            post_observation.save()

            post.save()

            for post_photo in post.post_photos.all():
                post.post_photos.remove(post_photo)

                post_photo.delete()

            for post_photo in post_photos:
                format, string = post_photo.split(";base64,")

                extension = format.split("/")[-1]

                post_photo = ContentFile(base64.b64decode(string), name = "POST " + str(post.id) + "." + extension)

                photo = PostPhoto.objects.create(post_photo = post_photo)
                    
                post.post_photos.add(photo)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostDraftSend(request, id):
    username = request.user.username

    post = Post.objects.get(id = id, user = request.user.user)
    
    post.post_status_id = 3

    post.save()

    curators = User.objects.filter(account__usertype_id = 2)

    for curator in curators:
        subject = "COTSEye has delivered an alert message!"

        scheme = request.scheme

        host = request.META["HTTP_HOST"]

        template = render_to_string("contributor/service/post/email.html", {"curator": curator.account.username, "contributor": post.user.account.username, "post": post, "scheme": scheme, "host": host})

        body = strip_tags(template)

        source = "COTSEye <settings.EMAIL_HOST_USER>"

        recipient = [curator.email]

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
        
    messages.success(request, username + ", " + "Your post has been successfully sent. Kindly wait for an approval email in the next 3 to 5 business days.")
    
    return redirect("Contributor Service Post")


def ContributorServicePostDraftSendFetch(request):
    if request.method == "POST":
        post = json.loads(request.body)

        for information in post:            
            post = Post.objects.filter(id = information.get("id"), user = information.get("user")).update(post_status_id = 3)
    
        curators = User.objects.filter(account__usertype_id = 2)

        for curator in curators:
            subject = "COTSEye has delivered an alert message!"

            scheme = request.scheme

            host = request.META["HTTP_HOST"]

            template = render_to_string("contributor/service/post/email.html", {"curator": curator.account.username, "contributor": post.user.account.username, "post": post, "scheme": scheme, "host": host})

            body = strip_tags(template)

            source = "COTSEye <settings.EMAIL_HOST_USER>"

            recipient = [curator.email]

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

        messages.success(request, username + ", " + "Your post has been successfully sent. Kindly wait for an approval email in the next 3 to 5 business days.")
    
        return redirect("Contributor Service Post")


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostDraftDelete(request, id):
    invalid_post = Post.objects.get(id = id, post_status = 4)

    if invalid_post.user == request.user.user:
        description = invalid_post.description

        coordinates = invalid_post.coordinates

        delete_post = Post.objects.filter(Q(description = description) & Q(coordinates = coordinates) & Q(post_status = 4))

        for invalid_post in delete_post:
            invalid_post.coordinates.delete()
        
            invalid_post.post_observation.delete()
        
            invalid_post.delete()

        username = request.user.username
        
        messages.success(request, username + ", " + "your post input has been successfully deleted.")
            
        return redirect("Contributor Service Post")

    else:
        messages.error(request, "Information input may not be vanished.")


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostDraftDeleteFetch(request):
    if request.method == "POST":
        post = json.loads(request.body)

        for information in post:            
            post = Post.objects.get(id = information.get("id"), user = information.get("user"))

            post.coordinates.delete()

            post.post_observation.delete()

            for post_photo in post.post_photos.all():
                post.post_photos.remove(post_photo)

                post_photo.delete()
            
            post.delete()


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlSighting(request):
    tab_number = 2

    sighting_number = 1

    notification_life = timezone.now() - timedelta(days = 30) 

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    posts = Post.objects.exclude(post_status = 4).order_by(
        Case(When(post_status = 3, then = 0), default = 1, output_field = IntegerField()),

        "-creation_date"
    )
    
    locations = Location.objects.all()

    municipalities = Municipality.objects.values('municipality_name').distinct()
    
    context = {"sighting_number": sighting_number, "tab_number": tab_number, "unread_notifications": unread_notifications, "posts": posts, "locations": locations, 'municipalities': municipalities}  
    
    return render(request, 'curator/control/sighting/sighting.html', context)


def CuratorControlSightingFetch(request, id):
    try:
        post = get_object_or_404(Post, id = id)
    
        post_data = {"id": post.id, "description": post.description, "coordinates": str(post.coordinates), "municipality":  str(post.location.municipality), "barangay":  str(post.location.barangay), "municipality":  str(post.location.municipality), "post_status": str(post.post_status), "size": str(post.post_observation.size), "density": str(post.post_observation.density), "weather": str(post.post_observation.weather), "depth": str(post.post_observation.depth), "remarks": post.remarks, "capture_date": post.capture_date.isoformat(), "creation_date": post.creation_date.isoformat(), "user": str(post.user), "validator": str(post.validator) if post.validator else None, "post_photos": [{"url": photo.post_photo.url, "id": photo.id} for photo in post.post_photos.all()]}
        
        return JsonResponse(post_data)
    
    except Post.DoesNotExist:
        return JsonResponse({"error": "The post could not be found."}, status = 404)
    

@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlSightingRead(request, id):
    notification_life = timezone.now() - timedelta(days = 30) 
    
    tab_number = 2

    sighting_number = 2

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    post = get_object_or_404(Post, id = id)

    other_posts = Post.objects.exclude(id = id).exclude(post_status = 4).order_by("-capture_date")[:5]

    post_photos = post.post_photos.all()

    other_photos = []

    locations = Location.objects.all()

    municipalities = Municipality.objects.all()

    for other_post in other_posts:
        first_photo = other_post.post_photos.first()

        other_photos.append({"post": other_post, "first_photo": first_photo})
    
    context = {"tab_number": tab_number, "sighting_number": sighting_number, "unread_notifications": unread_notifications, "post": post, "other_posts_with_photos": other_photos, "municipalities": municipalities, "post_photos": post_photos, "locations": locations}
    
    return render(request, "curator/control/sighting/read.html", context)


def CuratorControlSightingReadRedirect(request, id):
    object = Post.objects.get(id = id)

    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            return redirect(reverse("Curator Control Sighting Read", kwargs = {"object_id": object.id}))
        
        elif usertype == 2:
            return redirect(reverse("Curator Control Sighting Read", kwargs = {"object_id": object.id}))

        elif usertype == 1:
            return redirect(reverse("admin:reports_post_change", kwargs = {"object_id": object.id}))

    else:
        return redirect(reverse("Curator Control Sighting Read", kwargs = {"object_id": object.id}))
    

@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlSightingAdd(request, id):
    post = get_object_or_404(Post, id = id)

    if request.method == "POST":
        data = json.loads(request.body)
        
        remark = data.get("remark", "")

        post.remarks = remark
        
        post.save()
        
        return JsonResponse({"success": True, "message": "The remark has been successfully added."})
    
    return JsonResponse({"success": False, "message": "The remark could not be added. Kindly try again later."})


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlSightingUpdate(request, id):
    post = get_object_or_404(Post, id = id)

    data = {"latitude": post.location.latitude, "longitude": post.location.longitude, "location": {"municipality": post.location.municipality.municipality_name, "barangay": post.location.barangay.barangay_name}}
    
    return JsonResponse(data)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlSightingLocationUpdate(request, id):
    post = get_object_or_404(Post, id = id)

    data = json.loads(request.body)

    try:
        municipality = data.get("municipality")

        barangay = data.get("barangay")

        latitude = data.get("latitude")

        longitude = data.get("longitude")
        
        print(f"The received coordinates are {latitude}° N, and {longitude}° E.")

        coordinates_qs = Coordinates.objects.filter(latitude = latitude, longitude = longitude)

        if coordinates_qs.exists():
            coordinates = coordinates_qs.first()

        else:
            coordinates = Coordinates.objects.create(latitude = latitude, longitude = longitude)

        post.coordinates = coordinates

        print(f"The updated post coordinates are {post.coordinates.latitude}° N, and {post.coordinates.longitude}° E.")
        
        location = get_object_or_404(Location, municipality__municipality_name = municipality, barangay__barangay_name = barangay)

        post.location = location
        
        post.save()

        return JsonResponse({"status": "success"}, status = 200)
    
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status = 400)
    

@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlSightingValid(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        id = request.POST.get("post_id")

        post = get_object_or_404(Post, id = id)
        
        current_time = timezone.now()
       
        post.post_status = PostStatus.objects.get(id = 1)
        
        if request.user.usertype.id == 2:
            post.validator = request.user.user

        post.read_date = current_time
        
        post.save()

        return JsonResponse({"success": True, "message": "The post status has been successfully updated."})
    
    return JsonResponse({"success": False, "message": "The post status could not be updated. Kindly try again later."}, status = 400)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlSightingInvalid(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        id = request.POST.get("post_id")

        remarks = request.POST.get("remarks")
        
        post = get_object_or_404(Post, id = id)
               
        post.post_status = PostStatus.objects.get(id = 2)
        
        if request.user.usertype.id == 2:
            post.validator = request.user.user
        
        post.remarks = remarks 
        
        post.save()

        return JsonResponse({"success": True, "message": "The post status has been successfully updated."})
        
    return JsonResponse({"success": False, "message": "The post status could not be updated. Kindly try again later."}, status = 400)
    

@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlSightingDelete(request, id):
    if request.method == "DELETE":
        try:
            photo = get_object_or_404(PostPhoto, id = id)

            photo.delete()
            
            return JsonResponse({"success": True})
        
        except:
            return JsonResponse({"success": False}, status = 400)
        
    return JsonResponse({"success": False}, status = 405)


def PostValidReadRedirect(request, id):
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            object = Post.objects.get(id = id)

            return redirect(reverse("Contributor Service Post Feed Read", kwargs = {"id": object.id}))

        elif usertype == 2:
            object = Post.objects.get(id = id)

            return redirect(reverse("Curator Control Sighting Read", kwargs = {"id": object.id}))

        elif usertype == 1:
            object = Post.objects.get(id = id)

            return redirect(reverse("admin:reports_post_change", kwargs = {"object_id": object.id}))
    
    else:
        object = Post.objects.get(id = id)

        return redirect(reverse("Public Service Post Feed Read", kwargs = {"id": object.id}))