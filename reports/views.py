from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from reports.models import *
from reports.forms import CoordinatesForm, PostObservationsForm, PostForm
from authentications.views import ContributorCheck


# Create your views here.
@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorCreate(request):
    coordinates_form = CoordinatesForm()
    postobservations_form = PostObservationsForm()
    post_form = PostForm()
    
    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST)
        postobservations_form = PostObservationsForm(request.POST)
        post_form =  PostForm(request.POST, request.FILES)

        if coordinates_form.is_valid() and postobservations_form.is_valid() and post_form.is_valid():
            coordinates = coordinates_form.save(commit = False)
            post_observations = postobservations_form.save(commit = False)
            post = post_form.save(commit = False)
            user = request.user.user
            post_status = PostStatus.objects.get(id = 3)

            coordinates = Coordinates.objects.create(latitude = coordinates.latitude, longitude = coordinates.longitude)
            post_observations = PostObservations.objects.create(size = post_observations.size, depth = post_observations.depth, density = post_observations.density, weather = post_observations.weather)
            if Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and PostObservations.objects.filter(size = post_observations.size, depth = post_observations.depth, density = post_observations.density, weather = post_observations.weather).exists():
                Post.objects.create(user = user, description = post.description, date = post.date, post_photo = post.post_photo, coordinates = coordinates, post_status = post_status, post_observations = post_observations)

                username = request.user.username
                messages.success(request, username + ", " + "your information input was recorded for COTSEye.")
                return redirect("Contributor Home")
        
        else:
            messages.error(request, "Information input is not valid.")
            messages.error(request, coordinates_form.errors, postobservations_form.errors, post_form.errors)

    else:
        coordinates_form = CoordinatesForm()
        postobservations_form = PostObservationsForm()
        post_form = PostForm() 

    context = {"coordinates_form": coordinates_form, "postobservations_form": postobservations_form, "post_form": post_form}
    return render(request, "contributor/create.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorPost(request):
    uncertain_posts = Post.objects.filter(user = request.user.user, post_status = 3)

    try:
        uncertain_dates = Post.objects.filter(user = request.user.user, post_status = 3).latest("date")

    except:
        uncertain_dates = None

    valid_posts = Post.objects.filter(user = request.user.user, post_status = 1)

    try:
        valid_dates = Post.objects.filter(user = request.user.user, post_status = 1).latest("date")
        
    except:
        valid_dates = None

    invalid_posts = Post.objects.filter(user = request.user.user, post_status = 2)

    try:
        invalid_dates = Post.objects.filter(user = request.user.user, post_status = 2).latest("date")
        
    except:
        invalid_dates = None
    
    context = {"uncertain_posts": uncertain_posts, "uncertain_dates": uncertain_dates, "valid_posts": valid_posts, "valid_dates": valid_dates, "invalid_posts": invalid_posts, "invalid_dates": invalid_dates}
    return render(request, "contributor/post.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorUncertain(request):
    uncertain_posts = Post.objects.filter(user = request.user.user, post_status = 3)
    
    context = {"uncertain_posts": uncertain_posts}
    return render(request, "contributor/uncertain.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorUncertainRead(request, id):
    uncertain_posts = Post.objects.filter(id = id, user = request.user.user, post_status = 3)
    
    context = {"uncertain_posts": uncertain_posts}
    return render(request, "contributor/read.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorUncertainUpdate(request, id):
    uncertain_posts = Post.objects.get(id = id, post_status = 3)   

    if request.method == "POST":
        coordinates_form = CoordinatesForm(request.POST, instance = uncertain_posts.coordinates)
        postobservations_form = PostObservationsForm(request.POST, instance = uncertain_posts.post_observations)
        post_form =  PostForm(request.POST, request.FILES, instance = uncertain_posts)

        if coordinates_form.is_valid() and postobservations_form.is_valid() and post_form.is_valid():
            coordinates_form.save()
            postobservations_form.save()
            post_form.save()
            username = request.user.username
            messages.success(request, username + ", " + "your information input was recorded for COTSEye.")
            return redirect("Contributor Uncertain")
        
    else:
        coordinates_form = CoordinatesForm(instance = uncertain_posts.coordinates)
        postobservations_form = PostObservationsForm(instance = uncertain_posts.post_observations)
        post_form = PostForm(instance = uncertain_posts)       

    context = {"uncertain_posts": uncertain_posts, "coordinates_form": coordinates_form, "postobservations_form": postobservations_form, "post_form": post_form}
    return render(request, "contributor/update.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorValid(request):
    valid_posts = Post.objects.filter(user = request.user.user, post_status = 1)
    
    context = {"valid_posts": valid_posts}
    return render(request, "contributor/valid.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorValidRead(request, id):
    valid_posts = Post.objects.filter(id = id, user = request.user.user, post_status = 1)
    
    context = {"valid_posts": valid_posts}
    return render(request, "contributor/read.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorInvalid(request):
    invalid_posts = Post.objects.filter(user = request.user.user, post_status = 2)
    
    context = {"invalid_posts": invalid_posts}
    return render(request, "contributor/invalid.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorInvalidRead(request, id):
    invalid_posts = Post.objects.filter(id = id, user = request.user.user, post_status = 2)
    
    context = {"invalid_posts": invalid_posts}
    return render(request, "contributor/read.html", context)


@login_required(login_url = "Contributor Signin")
@user_passes_test(ContributorCheck, login_url = "Contributor Signin")
def ContributorInvalidDelete(request, id):
    invalid_posts = Post.objects.get(id = id, post_status = 2)

    if invalid_posts.user == request.user.user:
        invalid_posts.coordinates.delete()
        invalid_posts.post_observations.delete()
        invalid_posts.delete()

        username = request.user.username

        invalid_posts = Post.objects.filter(post_status = 2).count()
        if invalid_posts == 0:
            messages.success(request, username + ", " + "your information input was vanished from COTSEye.")
            return redirect("Contributor Post")
        
        elif invalid_posts >= 1:
            messages.success(request, username + ", " + "your information input was vanished from COTSEye.")
            return redirect("Contributor Invalid")

    else:
        messages.error(request, "Information input may not be vanished.")