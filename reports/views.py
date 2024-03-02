from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from reports.models import *
from reports.forms import CoordinatesForm, PostObservationForm, PostForm
from authentications.views import ContributorCheck


# Create your views here.
@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPost(request):
    valid_posts = Post.objects.filter(user = request.user.user, post_status = 1).distinct("description", "coordinates")

    try:
        valid_dates = Post.objects.filter(user = request.user.user, post_status = 1).latest("capture_date")
        
    except:
        valid_dates = None

    invalid_posts = Post.objects.filter(user = request.user.user, post_status = 2).distinct("description", "coordinates")

    try:
        invalid_dates = Post.objects.filter(user = request.user.user, post_status = 2).latest("capture_date")
        
    except:
        invalid_dates = None

    uncertain_posts = Post.objects.filter(user = request.user.user, post_status = 3).distinct("description", "coordinates")

    try:
        uncertain_dates = Post.objects.filter(user = request.user.user, post_status = 3).latest("capture_date")

    except:
        uncertain_dates = None
    
    context = {"valid_posts": valid_posts, "valid_dates": valid_dates, "invalid_posts": invalid_posts, "invalid_dates": invalid_dates, "uncertain_posts": uncertain_posts, "uncertain_dates": uncertain_dates}
    
    return render(request, "contributor/post/post.html", context)

@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostValid(request):
    valid_posts = Post.objects.filter(user = request.user.user, post_status = 1).distinct("description", "coordinates")
    
    context = {"valid_posts": valid_posts}
    
    return render(request, "contributor/post/valid.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostValidRead(request, id):
    valid_postss = Post.objects.filter(id = id, user = request.user.user, post_status = 1)
    
    context = {"valid_posts": valid_postss}
    
    return render(request, "contributor/read.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostInvalid(request):
    invalid_posts = Post.objects.filter(user = request.user.user, post_status = 2).distinct("description", "coordinates")
    
    context = {"invalid_posts": invalid_posts}
    
    return render(request, "contributor/post/invalid.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostInvalidRead(request, id):
    post = Post.objects.get(id = id, user = request.user.user, post_status = 2)

    invalid_post = Post.objects.filter(description = post.description, user = request.user.user, post_status = 2)
    
    context = {"post": post, "invalid_post": invalid_post}
    
    return render(request, "contributor/post/read.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostInvalidDelete(request, id):
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
            
        return redirect("Contributor Post Invalid")

    else:
        messages.error(request, "Information input may not be vanished.")

@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostUncertain(request):
    uncertain_posts = Post.objects.filter(user = request.user.user, post_status = 3).distinct("description", "coordinates")
    
    context = {"uncertain_posts": uncertain_posts}
    
    return render(request, "contributor/post/uncertain.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostUncertainCreate(request):
    context = {}
    
    return render(request, "contributor/post/create.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostUncertainCreateCapture(request):
    coordinates_form = CoordinatesForm()

    postobservation_form = PostObservationForm()

    depths = Depth.objects.all()

    weathers = Weather.objects.all()

    post_form = PostForm()
    
    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST)

        postobservation_form = PostObservationForm(request.POST)

        post_form =  PostForm(request.POST)

        if coordinates_form.is_valid() and postobservation_form.is_valid() and post_form.is_valid():
            coordinates = coordinates_form.save(commit = False)

            post_observation = postobservation_form.save(commit = False)

            post = post_form.save(commit = False)

            user = request.user.user

            post_status = PostStatus.objects.get(id = 3)

            coordinates = Coordinates.objects.create(latitude = coordinates.latitude, longitude = coordinates.longitude)
            
            depth = request.POST.get("depth")

            post_observation.depth = Weather.objects.get(id = depth)

            weather = request.POST.get("weather")

            post_observation.weather = Weather.objects.get(id = weather)

            post_observation = PostObservation.objects.create(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather)
            
            if Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and PostObservation.objects.filter(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather).exists():
                post_photos = request.FILES.getlist("post_photo")

                for post_photo in post_photos:
                    Post.objects.create(user = user, description = post.description, capture_date = post.capture_date, post_photo = post_photo, coordinates = coordinates, post_status = post_status, post_observation = post_observation)

                username = request.user.username
                
                messages.success(request, username + ", " + "your information input was recorded for COTSEye.")
                
                return redirect("Contributor Home")
        
        else:
            messages.error(request, "Information input is not valid.")
            
            messages.error(request, coordinates_form.errors, postobservation_form.errors, post_form.errors)

    else:
        coordinates_form = CoordinatesForm()
        
        postobservation_form = PostObservationForm()
        
        post_form = PostForm() 

    context = {"coordinates_form": coordinates_form, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/post/capture.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostUncertainCreateChoose(request):
    coordinates_form = CoordinatesForm()

    postobservation_form = PostObservationForm()

    depths = Depth.objects.all()

    weathers = Weather.objects.all()

    post_form = PostForm()
    
    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST)

        postobservation_form = PostObservationForm(request.POST)

        post_form =  PostForm(request.POST)

        if coordinates_form.is_valid() and postobservation_form.is_valid() and post_form.is_valid():
            coordinates = coordinates_form.save(commit = False)

            post_observation = postobservation_form.save(commit = False)

            post = post_form.save(commit = False)

            user = request.user.user

            post_status = PostStatus.objects.get(id = 3)

            coordinates = Coordinates.objects.create(latitude = coordinates.latitude, longitude = coordinates.longitude)
            
            depth = request.POST.get("depth")

            post_observation.depth = Weather.objects.get(id = depth)

            weather = request.POST.get("weather")

            post_observation.weather = Weather.objects.get(id = weather)

            post_observation = PostObservation.objects.create(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather)
            
            if Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and PostObservation.objects.filter(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather).exists():
                post_photos = request.FILES.getlist("post_photo")

                for post_photo in post_photos:
                    Post.objects.create(user = user, description = post.description, capture_date = post.capture_date, post_photo = post_photo, coordinates = coordinates, post_status = post_status, post_observation = post_observation)

                username = request.user.username
                
                messages.success(request, username + ", " + "your information input was recorded for COTSEye.")
                
                return redirect("Contributor Home")
        
        else:
            messages.error(request, "Information input is not valid.")
            
            messages.error(request, coordinates_form.errors, postobservation_form.errors, post_form.errors)

    else:
        coordinates_form = CoordinatesForm()
        
        postobservation_form = PostObservationForm()
        
        post_form = PostForm() 

    context = {"coordinates_form": coordinates_form, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/post/choose.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostUncertainRead(request, id):
    post = Post.objects.get(id = id, user = request.user.user, post_status = 3)

    uncertain_post = Post.objects.filter(description = post.description, user = request.user.user, post_status = 3)
    
    context = {"post": post, "uncertain_post": uncertain_post}
    
    return render(request, "contributor/post/read.html", context)


def ContributorPostUncertainUpdate(request):
    context = {}
    
    return render(request, "contributor/post/update.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostUncertainUpdateCapture(request, id):
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
           
            post_form.save()

            description = uncertain_post.description

            coordinates = uncertain_post.coordinates

            update_post = Post.objects.filter(Q(description = description) & Q(coordinates = coordinates))
            
            for uncertain_post in update_post.exclude(id = id):
                uncertain_post.coordinates = uncertain_post.coordinates

                uncertain_post.post_observation = uncertain_post.post_observation

                uncertain_post.save()

            username = request.user.username
            
            messages.success(request, username + ", " + "your information input was updated for COTSEye.")
            
            return redirect("Contributor Post Uncertain")

        else:
            messages.error(request, "Information input is not valid.")
            
            messages.error(request, coordinates_form.errors, postobservation_form.errors, post_form.errors)
        
    else:
        coordinates_form = CoordinatesForm(instance = uncertain_post.coordinates)
        
        postobservation_form = PostObservationForm(instance = uncertain_post.post_observation)
        
        post_form = PostForm(instance = uncertain_post)       

    context = {"uncertain_post": uncertain_post, "coordinates_form": coordinates_form, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/post/capture.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorPostUncertainUpdateChoose(request, id):
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
           
            post_form.save()

            description = uncertain_post.description

            coordinates = uncertain_post.coordinates

            update_post = Post.objects.filter(Q(description = description) & Q(coordinates = coordinates))
            
            for uncertain_post in update_post.exclude(id = id):
                uncertain_post.coordinates = uncertain_post.coordinates

                uncertain_post.post_observation = uncertain_post.post_observation

                uncertain_post.save()

            username = request.user.username
            
            messages.success(request, username + ", " + "your information input was updated for COTSEye.")
            
            return redirect("Contributor Post Uncertain")

        else:
            messages.error(request, "Information input is not valid.")
            
            messages.error(request, coordinates_form.errors, postobservation_form.errors, post_form.errors)
        
    else:
        coordinates_form = CoordinatesForm(instance = uncertain_post.coordinates)
        
        postobservation_form = PostObservationForm(instance = uncertain_post.post_observation)
        
        post_form = PostForm(instance = uncertain_post)       

    context = {"uncertain_post": uncertain_post, "coordinates_form": coordinates_form, "depths": depths, "weathers": weathers, "postobservation_form": postobservation_form, "post_form": post_form}
    
    return render(request, "contributor/post/choose.html", context)