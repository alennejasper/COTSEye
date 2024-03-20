from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.urls import reverse
from authentications.models import Account
from reports.models import *
from reports.forms import CoordinatesForm, PostObservationForm, PostForm
from authentications.views import ContributorCheck, OfficerCheck, AdministratorCheck


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

        post_form =  PostForm(request.POST)

        if coordinates_form.is_valid() and postobservation_form.is_valid() and post_form.is_valid():
            coordinates = coordinates_form.save(commit = False)

            post_observation = postobservation_form.save(commit = False)

            post = post_form.save(commit = False)

            user = request.user.user

            post_status = PostStatus.objects.get(id = 3)

            coordinates = Coordinates.objects.create(latitude = coordinates.latitude, longitude = coordinates.longitude)
            
            depth = request.POST.get("depth")

            post_observation.depth = Depth.objects.get(id = depth)

            weather = request.POST.get("weather")

            post_observation.weather = Weather.objects.get(id = weather)

            post_observation = PostObservation.objects.create(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather)
            
            if Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and PostObservation.objects.filter(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather).exists():
                post = Post.objects.create(user = user, description = post.description, capture_date = post.capture_date, coordinates = coordinates, post_status = post_status, post_observation = post_observation)

                post_photos = request.FILES.getlist("post_photo")

                for post_photo in post_photos:
                    photo = PostPhotos.objects.create(post_photo = post_photo)
                    
                    post.post_photos.add(photo)

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

        post_form =  PostForm(request.POST)

        if coordinates_form.is_valid() and postobservation_form.is_valid() and post_form.is_valid():
            coordinates = coordinates_form.save(commit = False)

            post_observation = postobservation_form.save(commit = False)

            post = post_form.save(commit = False)

            user = request.user.user

            post_status = PostStatus.objects.get(id = 3)

            coordinates = Coordinates.objects.create(latitude = coordinates.latitude, longitude = coordinates.longitude)
            
            depth = request.POST.get("depth")

            post_observation.depth = Depth.objects.get(id = depth)

            weather = request.POST.get("weather")

            post_observation.weather = Weather.objects.get(id = weather)

            post_observation = PostObservation.objects.create(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather)
            
            if Coordinates.objects.filter(latitude = coordinates.latitude, longitude = coordinates.longitude).exists() and PostObservation.objects.filter(size = post_observation.size, depth = post_observation.depth, density = post_observation.density, weather = post_observation.weather).exists():
                post = Post.objects.create(user = user, description = post.description, capture_date = post.capture_date, coordinates = coordinates, post_status = post_status, post_observation = post_observation)

                post_photos = request.FILES.getlist("post_photo")

                for post_photo in post_photos:
                    photo = PostPhotos.objects.create(post_photo = post_photo)
                    
                    post.post_photos.add(photo)

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
                photo = PostPhotos.objects.create(post_photo = post_photo)

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
                photo = PostPhotos.objects.create(post_photo = post_photo)

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

    valid_posts = Post.objects.filter(user = request.user.user, post_status = 1)
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        if "from_date" in request.GET or "to_date" in request.GET:
            if from_date and to_date:
                valid_posts = Post.objects.filter(user = request.user.user, post_status = 1, capture_date__range = [from_date, to_date])

                if not valid_posts:
                    username = request.user.username

                    messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

            elif not from_date and not to_date:
                messages.error(request, "Date range is not valid.")

            elif not from_date or not to_date:
                messages.error(request, "Date range is not valid.")

        elif not valid_posts:
            username = request.user.username

            messages.error(request, username + ", " + "your information input is empty within COTSEye.")

    context = {"username": username, "valid_posts": valid_posts}
    
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

    invalid_posts = Post.objects.filter(user = request.user.user, post_status = 2)
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        if "from_date" in request.GET or "to_date" in request.GET:
            if from_date and to_date:
                invalid_posts = Post.objects.filter(user = request.user.user, post_status = 2, capture_date__range = [from_date, to_date])
            
                if not invalid_posts:
                    username = request.user.username

                    messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

            elif not from_date and not to_date:
                messages.error(request, "Date range is not valid.")

            elif not from_date or not to_date:
                messages.error(request, "Date range is not valid.")
            
            if not invalid_posts:
                username = request.user.username

                messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

        elif not invalid_posts:
            username = request.user.username

            messages.error(request, username + ", " + "your information input is empty within COTSEye.")

    context = {"username": username, "invalid_posts": invalid_posts}
    
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

    uncertain_posts = Post.objects.filter(user = request.user.user, post_status = 3)
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")
        
        to_date = request.GET.get("to_date")

        if "from_date" in request.GET or "to_date" in request.GET:
            if from_date and to_date:
                uncertain_posts = Post.objects.filter(user = request.user.user, post_status = 3, capture_date__range = [from_date, to_date])
            
                if not uncertain_posts:
                    username = request.user.username

                    messages.error(request, username + ", " + "information input cannot be found within COTSEye.")

            elif not from_date and not to_date:
                messages.error(request, "Date range is not valid.")

            elif not from_date or not to_date:
                messages.error(request, "Date range is not valid.")
        
        elif not uncertain_posts:
            username = request.user.username

            messages.error(request, username + ", " + "your information input is empty within COTSEye.")

    context = {"username": username, "uncertain_posts": uncertain_posts}
    
    return render(request, "contributor/service/post/uncertain.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServicePostUncertainRead(request, id):
    username = request.user.username

    uncertain_post = Post.objects.get(id = id, user = request.user.user, post_status = 3)
    
    context = {"username": username, "uncertain_post": uncertain_post}
    
    return render(request, "contributor/service/post/read.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatisticsPost(request):
    username = request.user.username

    options = Post.objects.all()

    records = Post.objects.all()
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        user = request.GET.get("user")

        post_status = request.GET.get("post_status")

        depth = request.GET.get("depth")

        weather = request.GET.get("weather")

        results = None

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

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")


    context = {"username": username, "options": options, "records": records, "results": results}

    return render(request, "officer/control/post/post.html", context)


@login_required(login_url = "Administrator Control Login")
@user_passes_test(AdministratorCheck, login_url = "Administrator Control Login")
def AdministratorControlStatisticsPost(request):
    username = request.user.username

    options = Post.objects.all()

    records = Post.objects.all()
    
    if request.method == "GET":
        from_date = request.GET.get("from_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        to_date = request.GET.get("to_date")

        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        user = request.GET.get("user")

        post_status = request.GET.get("post_status")

        depth = request.GET.get("depth")

        weather = request.GET.get("weather")

        results = None

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

        elif not results:
            username = request.user.username

            messages.error(request, username + ", " + "information input is impossible within COTSEye.")


    context = {"username": username, "options": options, "records": records, "results": results}

    return render(request, "admin/control/post/post.html", context)


def ServicePostValidReadRedirect(request):
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
    usertype = request.user.usertype_id

    object = Post.objects.get(id = object_id)

    if usertype == 2:
        return redirect(reverse("officer:reports_post_change", kwargs = {"object_id": object.id}))

    if usertype == 1:
        return redirect(reverse("admin:reports_post_change", kwargs = {"object_id": object.id}))