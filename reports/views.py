from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from authentications.models import Account
from authentications.views import ContributorCheck, OfficerCheck
from managements.models import Location
from reports.models import *
from reports.forms import CoordinatesForm, PostObservationForm, PostForm
from django.utils import timezone
from datetime import timedelta

import base64
import datetime
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

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    locations = Location.objects.all()

    municipalities = Location.objects.values("municipality").distinct()

    coordinates_form = CoordinatesForm()

    postobservation_form = PostObservationForm()

    sizes = Size.objects.all()

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

            action = request.POST.get("action")

            if action == "save and submit":
                post_status = PostStatus.objects.get(id = 3)

            elif action == "save as draft":
                post_status = PostStatus.objects.get(id = 4)

            coordinates = Coordinates.objects.create(latitude = coordinates.latitude, longitude = coordinates.longitude)
            
            size = request.POST.get("size")

            try:
                post_observation.size = Size.objects.get(id = size)

            except:
                post_observation.size = None

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

            location = request.POST.get("barangay")

            try:
                post.location = Location.objects.get(id = location)

            except:
                post.location = None

            post_observation = PostObservation.objects.create(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather)
            
            if Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and PostObservation.objects.filter(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather).exists():
                post = Post.objects.create(user = user, description = post.description, capture_date = post.capture_date, coordinates = coordinates, location = post.location, post_status = post_status, post_observation = post_observation)
                
                post_photos_capture = request.FILES.getlist("post_photos_capture")

                post_photos_choose = request.FILES.getlist("post_photos_choose")

                post_photos = post_photos_capture + post_photos_choose

                for post_photo in post_photos:
                    photo = PostPhoto.objects.create(post_photo = post_photo)
                    
                    post.post_photos.add(photo)

                username = request.user.username
                
                messages.success(request, f"{username}, For verification and will be approved by the administrator. You will be notified in 3 to 5 business days.")
                
                return redirect("Contributor Service Post")

            else:
                messages.error(request, "Information input is not valid.")
        
        else:
            messages.error(request, "Information input is not valid.")
            
            messages.error(request, coordinates_form.errors, postobservation_form.errors, post_form.errors)

    else:
        coordinates_form = CoordinatesForm()
        
        postobservation_form = PostObservationForm()
        
        post_form = PostForm() 

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "locations": locations, "municipalities": municipalities, "coordinates_form": coordinates_form, "sizes": sizes, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/service/report/report.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceReportFetch(request):
    if request.method == "POST":
        information = json.loads(request.body)

        for information in information:
            user = information.get("user")

            user = User.objects.get(id = user)

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

            weather = Weather.objects.get(id = weather) if weather else None

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

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

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

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

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

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    valid_posts = Post.objects.filter(post_status = 1).order_by("-creation_date")

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "valid_posts": valid_posts}
    
    return render(request, "contributor/service/post/feed.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostFeedRead(request, id):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

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

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    draft_post = get_object_or_404(Post, id = id, post_status = 4)

    locations = Location.objects.all()

    municipalities = Location.objects.values("municipality").distinct()

    sizes = Size.objects.all()

    depths = Depth.objects.all()

    weathers = Weather.objects.all()

    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST, instance = draft_post.coordinates)

        postobservation_form = PostObservationForm(request.POST, instance = draft_post.post_observation)

        post_form = PostForm(request.POST, request.FILES, instance=draft_post)

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

            messages.success(request, username + ", " + "your information input was updated for COTSEye.")

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

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "draft_post": draft_post, "locations": locations, "municipalities": municipalities, "coordinates_form": coordinates_form, "sizes": sizes, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}

    return render(request, "contributor/service/report/report.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostDraftUpdateFetch(request):
    if request.method == "POST":
        information = json.loads(request.body)

        for information in information:
            id = information.get("id")

            user = information.get("user")

            user = User.objects.get(id = user)

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

            weather = Weather.objects.get(id = weather) if weather else None

            location = Weather.objects.get(id = location) if location else None

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

    officers = User.objects.filter(account__usertype_id = 2)

    for officer in officers:
        subject = "COTSEye has delivered an alert message!"

        scheme = request.scheme

        host = request.META["HTTP_HOST"]

        template = render_to_string("webwares/email.html", {"officer": officer.account.username, "contributor": post.user.account.username, "post": post, "scheme": scheme, "host": host})

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
        
    messages.success(request, username + ", " + "your information input was sent to COTSEye.")
    
    return redirect("Contributor Service Post")


def ContributorServicePostDraftSendFetch(request):
    if request.method == "POST":
        post = json.loads(request.body)

        for information in post:            
            post = Post.objects.filter(id = information.get("id"), user = information.get("user")).update(post_status_id = 3)
    
        officers = User.objects.filter(account__usertype_id = 2)

        for officer in officers:
            subject = "COTSEye has delivered an alert message!"

            scheme = request.scheme

            host = request.META["HTTP_HOST"]

            template = render_to_string("webwares/email.html", {"officer": officer.account.username, "contributor": post.user.account.username, "post": post, "scheme": scheme, "host": host})

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

        messages.success(request, username + ", " + "your information input was sent to COTSEye.")
    
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
        
        messages.success(request, username + ", " + "your information input was vanished from COTSEye.")
            
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


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlSighting(request):
    notification_life = timezone.now() - timedelta(days = 30) 

    unread_notifications = Post.objects.filter(read_status = False, creation_date__gte=notification_life).order_by("-creation_date")[:5]

    posts = Post.objects.exclude(post_status = 4).order_by('-creation_date')

    locations = Location.objects.all()

    municipalities = Location.objects.values('municipality').distinct()
    
    context = {"unread_notifications": unread_notifications, "posts": posts, "locations": locations, 'municipalities': municipalities,}  
    
    return render(request, 'officer/control/sighting/sighting.html', context)



@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def add_remark(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        remark = data.get('remark', '')
        post.remarks = remark
        post.save()
        return JsonResponse({'success': True, 'message': 'Remark added successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlSightingUpdate(request, id):
    post = get_object_or_404(Post, id=id)
    data = {
        "latitude": post.location.latitude,
        "longitude": post.location.longitude,
        "location": {
            "municipality": post.location.municipality,
            "barangay": post.location.barangay
        }
    }
    return JsonResponse(data)


@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    data = json.loads(request.body)

    try:
        # Retrieve data from the request
        municipality = data.get('municipality')
        barangay = data.get('barangay')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Log received coordinates for debugging
        print(f"Received coordinates: {latitude}° N, {longitude}° E")

        # Update coordinates
        coordinates_qs = Coordinates.objects.filter(latitude=latitude, longitude=longitude)

        if coordinates_qs.exists():
            coordinates = coordinates_qs.first()
        else:
            coordinates = Coordinates.objects.create(latitude=latitude, longitude=longitude)

        post.coordinates = coordinates

        # Log the post's updated coordinates
        print(f"Updated post coordinates: {post.coordinates.latitude}° N, {post.coordinates.longitude}° E")
        
        # Update location
        location = get_object_or_404(Location, municipality=municipality, barangay=barangay)
        post.location = location
        
        post.save()

        return JsonResponse({'status': 'success'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def mark_post_as_read(request, id):
    post = Post.objects.get(id = id)

    post.read_status = True

    post.read_date = timezone.now()

    if request.user.usertype.id == 2:
        post.validated_by = request.user.user
        
    print(post.read_status, post.read_date, post.validated_by)

    post.save()

    return redirect("post_list")


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlSightingRead(request, id):
    notification_life = timezone.now() - timedelta(days = 30) 

    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by("-creation_date")[:5]

    post = get_object_or_404(Post, id = id)

    other_posts = Post.objects.exclude(id = id).exclude(post_status = 4).order_by("-capture_date")[:5]

    post_photos = post.post_photos.all()

    other_photos = []

    locations = Location.objects.all()

    municipalities = Location.objects.values('municipality').distinct()


    for other_post in other_posts:
        first_photo = other_post.post_photos.first()

        other_photos.append({"post": other_post, "first_photo": first_photo})
    
    context = {"unread_notifications": unread_notifications, "post": post, "other_posts_with_photos": other_photos, 'municipalities': municipalities, "post_photos": post_photos, "locations": locations}
    
    return render(request, "officer/control/sighting/read.html", context)


def OfficerControlSightingReadRedirect(request, object_id):
    object = Post.objects.get(id = object_id)

    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            return redirect(reverse("Officer Control Sighting Read", kwargs = {"object_id": object.id}))
        
        elif usertype == 2:
            return redirect(reverse("Officer Control Sighting Read", kwargs = {"object_id": object.id}))

        elif usertype == 1:
            return redirect(reverse("admin:reports_post_change", kwargs = {"object_id": object.id}))

    else:
        return redirect(reverse("Officer Control Sighting Read", kwargs = {"object_id": object.id}))
    

@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def DeletePostPhoto(request, photo_id):
    if request.method == 'DELETE':
        try:
            photo = get_object_or_404(PostPhoto, id=photo_id)
            photo.delete()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False}, status=400)
    return JsonResponse({'success': False}, status=405)


@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def OfficerControlSightingValid(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        id = request.POST.get("post_id")

        post = get_object_or_404(Post, id=id)
        
        current_time = timezone.now()
       
        post.post_status = PostStatus.objects.get(id=1)
        
        if request.user.usertype.id == 2:
            post.validated_by = request.user.user

        post.read_date = current_time  # Update the read_date to current time
        
        post.save()
        return JsonResponse({"success": True, "message": "Post status updated successfully. Read Date updated"})
    
       

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

@login_required(login_url="Officer Control Login")
@user_passes_test(OfficerCheck, login_url="Officer Control Login")
def OfficerControlSightingInvalid(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        id = request.POST.get("post_id")
        remarks = request.POST.get("remarks")
        
        post = get_object_or_404(Post, id=id)
        
        current_time = timezone.now()
       

        if post.read_date is None:
            post.post_status = PostStatus.objects.get(id=2)
            
            if request.user.usertype.id == 2:
                post.validated_by = request.user.user
            
            post.remarks = remarks  # Save the remarks
            post.read_date = current_time  # Update the read_date to current time
            
            post.save()
            return JsonResponse({"success": True, "message": "Post status updated to invalid with remarks. Read Date updated."})
        

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
    

def PostValidReadRedirect(request, id):
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 3:
            object = Post.objects.get(id = id)

            return redirect(reverse("Contributor Service Post Feed Read", kwargs = {"id": object.id}))

        elif usertype == 2:
            object = Account.objects.get(id = request.user.id)

            return redirect(reverse("Officer Control Sighting Read", kwargs = {"id": object.id}))

        elif usertype == 1:
            object = Account.objects.get(id = request.user.id)

            return redirect(reverse("admin:reports_post_change", kwargs = {"object_id": object.id}))
    
    else:
        object = Post.objects.get(id = id)

        return redirect(reverse("Public Service Post Feed Read", kwargs = {"id": object.id}))