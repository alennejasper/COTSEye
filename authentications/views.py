from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.socialaccount.signals import social_account_updated
from authentications.forms import AccountForm, UserForm, ProfileForm
from authentications.models import *
from auxiliaries.models import Announcement
from managements.models import Status, Intervention, Location
from reports.models import Post
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.db.models import Max

import base64
import json


# Create your views here.
def PublicServiceHome(request):
    user = request.user

    username = "public/everyone"

    latest_announcements = Announcement.objects.all().order_by("-release_date")[:3]

    valid_posts = Post.objects.filter(post_status = 1).order_by("-capture_date")[:3]

    if user.is_authenticated:
        if user.usertype_id == 3:
            return redirect("Contributor Service Home")
        
        elif user.usertype_id == 2:
            return redirect("Officer Control Home")
        
        elif user.usertype_id == 1:
            return redirect("admin:index")

    else:
        try:
            map_posts = Post.objects.filter(post_status = 1)

            map_statuses = Status.objects.all()
    
        except:
            map_posts = None

            map_statuses = None

    if not any(message.level in [messages.INFO, messages.SUCCESS, messages.ERROR] for message in messages.get_messages(request)):
        messages.info(request, username + ", " + "kindly see announcements within COTSEye to check for updates today.")

    context = {"username": username, "map_posts": map_posts, "map_statuses": map_statuses, "latest_announcements": latest_announcements, "valid_posts": valid_posts}
    
    return render(request, "public/service/home/home.html", context)


def PublicServiceFallback(request):
    public = "public/everyone"

    fallback = "The COTSEye cannot keep in touch to the requested page today, as such is not found within the cache storage."

    context = {"public": public, "fallback": fallback}
    
    return render(request, "public/service/fallback/fallback.html", context)


def ContributorServiceRegister(request):
    account_form = AccountForm()

    user_form = UserForm()

    if request.method == "POST":
        account_form = AccountForm(request.POST)

        user_form = UserForm(request.POST)

        if account_form.is_valid() and user_form.is_valid():
            account = account_form.save(commit = False)

            user = user_form.save(commit = False)

            usertype = UserType.objects.get(id = 3)

            account = Account.objects.create(username = account.username, password = account.password, usertype = usertype)
            
            if Account.objects.filter(username = account.username, password = account.password, usertype = usertype).exists():
                User.objects.create(account = account, first_name = user.first_name, last_name = user.last_name, email = user.email, phone_number = user.phone_number)
                
                username = account.username
                
                messages.success(request, username + ", " + "your information input was recorded online for COTSEye.")
                
                return redirect("Contributor Service Login")
        
        else:
            messages.error(request, "Username exists or is not valid, or passwords are short, entirely numeric, or do not match.")
            
            messages.error(request, account_form.errors, user_form.errors) 

    else:
        account_form = AccountForm()
        
        user_form = UserForm()

    context = {"account_form": account_form, "user_form": user_form}
    
    return render(request, "contributor/service/register/register.html", context)


def ContributorServiceLogin(request):
    @receiver(social_account_updated)
    def UpdateUser(sender, request, sociallogin, **kwargs):
        if sociallogin.account.provider == "google":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 2:
                messages.error(request, "Username or password is not valid.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Contributor Service Login")
            
            else:
                if sociallogin.account.provider == "google":
                    user = sociallogin.user
                    
                    user.usertype_id = 3

                    if "email" in sociallogin.account.extra_data:
                        email = sociallogin.account.extra_data["email"]
                        
                        username = email.split("@")[0]
                        
                        sociallogin.account.user.username = username
                        
                        instance, created = User.objects.get_or_create(account = user, email = email)

                        instance.first_name = sociallogin.account.extra_data.get("given_name", None)
                        
                        instance.last_name = sociallogin.account.extra_data.get("family_name", None)

                        instance.save()
                        
                        sociallogin.account.user.save()

                    user.save()
        
        elif sociallogin.account.provider == "facebook":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 2:
                messages.error(request, "Username or password is not valid.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Contributor Service Login")
            
            else:
                if sociallogin.account.provider == "facebook":
                    user = sociallogin.user
                    
                    user.usertype_id = 3

                    if "email" in sociallogin.account.extra_data:
                        email = sociallogin.account.extra_data["email"]
                       
                        username = email.split("@")[0]
                        
                        sociallogin.account.user.username = username
                       
                        instance, created = User.objects.get_or_create(account = user, email = email)

                        instance.first_name = sociallogin.account.extra_data.get("first_name", None)
                        
                        instance.last_name = sociallogin.account.extra_data.get("last_name", None)

                        instance.save()
                        
                        sociallogin.account.user.save()

                    user.save()
    
    social_account_updated.connect(UpdateUser, sender = None)
     
    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")

        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 3:
                login(request, account)
                
                return redirect("Contributor Service Home")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "contributor/service/login/login.html", context)


def ContributorServiceLoginFacebook(request):
    username = request.user.username

    messages.info(request, username + ", " + "kindly login again in order to be validated by COTSEye today.")

    if request.method == "POST":
        username = request.POST.get("username")

        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 3:
                login(request, account)

                return redirect("Contributor Service Home")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "contributor/service/login/facebook.html", context)


def ContributorServiceLoginGoogle(request):
    username = request.user.username

    messages.info(request, username + ", " + "kindly login again in order to be validated by COTSEye today.")

    if request.method == "POST":
        username = request.POST.get("username")

        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 3:
                login(request, account)

                return redirect("Contributor Service Home")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "contributor/service/login/google.html", context)


def ContributorCheck(account):
    try:
        return account.is_authenticated and account.usertype_id == 3 != None
    
    except Account.DoesNotExist:
            return False


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceHome(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)
    
    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    latest_announcements = Announcement.objects.all().order_by("-release_date")[:3]

    valid_posts = Post.objects.filter(post_status = 1).order_by("-capture_date")[:3]
            
    try:
        map_posts = Post.objects.filter(post_status = 1)

        map_statuses = Status.objects.all()

    except:
        map_posts = None

        map_statuses = None
    
    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "map_posts": map_posts, "map_statuses": map_statuses, "latest_announcements": latest_announcements, "valid_posts": valid_posts}

    return render(request, "contributor/service/home/home.html", context)
    

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceNotification(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    unread_items = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")

    read_items = Post.objects.filter(contrib_read_status = True).filter(contrib_read_date__gte = timezone.now() - timedelta(days = 30), contrib_read_date__lte = timezone.now()).order_by("-creation_date")
            
    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "unread_items": unread_items, "read_items": read_items}
    
    return render(request, "contributor/service/notification/notification.html", context)


def ContributorServiceNotificationMark(request, id):
    try:
        post = Post.objects.get(id = id)

        post.contrib_read_status = True

        post.contrib_read_date = timezone.now()

        post.save()

        return redirect("Contributor Service Notification") 
    
    except Post.DoesNotExist:
        return JsonResponse({"success": False, "error": "COTSEye cannot find the post."})
    

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceProfile(request):
    user = User.objects.get(account = request.user)

    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    context = {"user": user, "username": username, "user_profile": user_profile, "unread_notifications": unread_notifications}

    return render(request, "contributor/service/profile/profile.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceProfileUpdate(request):
    user = User.objects.get(account = request.user)

    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    unread_notifications = Post.objects.filter(contrib_read_status = False, user = request.user.user).order_by("-creation_date")[:3]

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance = request.user.user)
        
        if profile_form.is_valid():
            profile_form.save()

            username = request.user.username

            messages.success(request, username + ", " + "your information input was recorded online for COTSEye.")
            
            return redirect("Contributor Service Home")
            
    else:
        profile_form = ProfileForm(request.user.user)

    context = {"user": user, "username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "profile_form": profile_form}
    
    return render(request, "contributor/service/profile/update.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceProfileUpdateFetch(request):
    if request.method == "POST":
        information = json.loads(request.body)

    for information in information:
        account = information.get("account")

        account = Account.objects.get(id = account)

        first_name = information.get("first_name")

        last_name = information.get("last_name")

        profile_photo = information.get("profile_photo")

        format, string = profile_photo.split(";base64,")

        extension = format.split("/")[-1]

        profile_photo = ContentFile(base64.b64decode(string), name = "POST " + str(user.id) + "." + extension)

        email = information.get("email")

        phone_number = information.get("phone_number")

        user = User.objects.get(account = account)

        user.first_name = first_name

        user.last_name = last_name

        user.profile_photo = profile_photo

        user.email = email
        
        user.phone_number = phone_number
                

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceFallback(request):
    contributor = request.user.username

    contributor_profile = User.objects.get(account = request.user)

    fallback = "The COTSEye cannot keep in touch to the requested page today, as such is not found within the cache storage."

    context = {"contributor": contributor, "contributor_profile": contributor_profile, "fallback": fallback}
    
    return render(request, "contributor/service/fallback/fallback.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceLogout(request):
    username = request.user.username

    logout(request)
    
    messages.success(request, username + ", " + "your account used just now was signed out of COTSEye.")
    
    return redirect("Public Service Home")


def OfficerControlRegister(request):
    account_form = AccountForm()

    user_form = UserForm()

    if request.method == "POST":
        account_form = AccountForm(request.POST)

        user_form = UserForm(request.POST)

        if account_form.is_valid() and user_form.is_valid():
            account = account_form.save(commit = False)

            user = user_form.save(commit = False)

            usertype = UserType.objects.get(id = 2)

            account = Account.objects.create(username = account.username, password = account.password, usertype = usertype)
            
            if Account.objects.filter(username = account.username, password = account.password, usertype = usertype).exists():
                User.objects.create(account = account, first_name = user.first_name, last_name = user.last_name, email = user.email, phone_number = user.phone_number)
                
                username = account.username
                
                messages.success(request, username + ", " + "your information input was recorded online for COTSEye.")
                
                return redirect("Officer Control Login")
        
        else:
            messages.error(request, "Username exists or is not valid, or passwords are short, entirely numeric, or do not match.")
            
            messages.error(request, account_form.errors, user_form.errors)  

    else:
        account_form = AccountForm()
        
        user_form = UserForm()

    context = {"account_form": account_form, "user_form": user_form}
    
    return render(request, "officer/control/register/register.html", context)


def OfficerControlLogin(request):
    @receiver(social_account_updated)
    def UpdateUser(sender, request, sociallogin, **kwargs):
        if sociallogin.account.provider == "google":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 3:
                messages.error(request, "Username or password is not valid.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Officer Control Login")
            
            else:
                if sociallogin.account.provider == "google":
                    user = sociallogin.user
                    
                    user.usertype_id = 2

                    if "email" in sociallogin.account.extra_data:
                        email = sociallogin.account.extra_data["email"]
                        
                        username = email.split("@")[0]
                        
                        sociallogin.account.user.username = username
                        
                        instance, created = User.objects.get_or_create(account = user, email = email)

                        instance.first_name = sociallogin.account.extra_data.get("given_name", None)
                        
                        instance.last_name = sociallogin.account.extra_data.get("family_name", None)

                        instance.save()
                        
                        sociallogin.account.user.save()

                    user.save()
        
        elif sociallogin.account.provider == "facebook":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 3:
                messages.error(request, "Username or password is not valid.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Officer Control Login")
            
            else:
                if sociallogin.account.provider == "facebook":
                    user = sociallogin.user
                    
                    user.usertype_id = 2

                    if "email" in sociallogin.account.extra_data:
                        email = sociallogin.account.extra_data["email"]
                        
                        username = email.split("@")[0]
                        
                        sociallogin.account.user.username = username
                        
                        instance, created = User.objects.get_or_create(account = user, email = email)

                        instance.first_name = sociallogin.account.extra_data.get("first_name", None)
                        
                        instance.last_name = sociallogin.account.extra_data.get("last_name", None)

                        instance.save()
                        
                        sociallogin.account.user.save()

                    user.save()
    
    social_account_updated.connect(UpdateUser, sender = None)

    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")

        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 2:
                login(request, account)
                
                return redirect("Officer Control Home")
            
            else:
                messages.error(request, "Username or password is not valid.")

        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "officer/control/login/login.html", context)


def OfficerControlLoginFacebook(request):
    username = request.user.username

    messages.info(request, username + ", " + "kindly login again in order to be validated by COTSEye today.")

    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 2:
                login(request, account)
                
                return redirect("Officer Control Home")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}
    
    return render(request, "officer/control/login/facebook.html", context)


def OfficerControlLoginGoogle(request):
    username = request.user.username

    messages.info(request, username + ", " + "kindly login again in order to be validated by COTSEye today.")
    
    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 2:
                login(request, account)
                
                return redirect("Officer Control Home")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}
    
    return render(request, "officer/control/login/google.html", context)


def OfficerCheck(account):
    try:
        return account.is_authenticated and account.usertype_id == 2 != None
    
    except Account.DoesNotExist:
            return False
    

@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlHome(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    unread_notifications = Post.objects.filter(read_status = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    municipality_filter = request.GET.get("municipality")

    barangay_filter = request.GET.get("barangay")

    year_filter = request.GET.get("year")

    latest_statuses = Status.objects.values("location__municipality").annotate(max_onset_date = Max("onset_date"))

    latest_status_entries = Status.objects.filter(location__municipality__in = [status["location__municipality"] for status in latest_statuses], onset_date__in = [status["max_onset_date"] for status in latest_statuses]).order_by("location__municipality").distinct("location__municipality")

    status_data = []

    for status_entry in latest_status_entries:
        status_data.append({"municipality": status_entry.location.municipality, "caught_amount": status_entry.caught_overall, "volunteer_amount": status_entry.volunteer_overall, "status_type": str(status_entry.statustype), "intervention_date": status_entry.onset_date.strftime("%m/%d/%Y")})

    municipalities = Location.objects.values("municipality").distinct()

    barangays = Location.objects.filter(municipality = municipality_filter).values("barangay").distinct() if municipality_filter else []

    locations_query = Location.objects.all()

    if municipality_filter:
        locations_query = locations_query.filter(municipality = municipality_filter)
        
    else:
        municipality_filter = "Alabel"
        locations_query = locations_query.filter(municipality = municipality_filter)

    if barangay_filter:
        locations_query = locations_query.filter(barangay = barangay_filter)

    else:
        barangay_filter = "Kawas"
        locations_query = locations_query.filter(barangay = barangay_filter)

    locations = locations_query.distinct()

    data = []

    total_caught_overall = 0

    for location in locations:
        interventions_query = Intervention.objects.filter(location = location).order_by("intervention_date")

        if year_filter:
            start_date = datetime.strptime(year_filter, "%Y").replace(month = 1, day = 1)

            end_date = datetime.strptime(year_filter, "%Y").replace(month = 12, day = 31)

            interventions_query = interventions_query.filter(intervention_date__range = [start_date, end_date])

        else:
            start_date = datetime.strptime("2024", "%Y").replace(month = 1, day = 1)

            end_date = datetime.strptime("2024", "%Y").replace(month = 12, day = 31)

            interventions_query = interventions_query.filter(intervention_date__range = [start_date, end_date])

        intervention_dates = []

        caught_overalls = []
        
        titles = []
        
        status_types = []
        
        volunteer_amounts = []
        
        caught_overall_sum = 0

        for intervention in interventions_query:
            if intervention.statustype:
                intervention_dates.append(intervention.intervention_date.strftime("%Y-%m-%d"))

                caught_overalls.append(intervention.caught_amount)
                
                titles.append(intervention.title)
                
                status_types.append(str(intervention.statustype))
                
                volunteer_amounts.append(intervention.volunteer_amount)
                
                caught_overall_sum += intervention.caught_amount

        total_caught_overall += caught_overall_sum

        if intervention_dates:
            min_date = datetime.strptime(intervention_dates[0], "%Y-%m-%d")

            max_date = datetime.strptime(intervention_dates[-1], "%Y-%m-%d")
            
            current_date = min_date
            
            date_set = set(intervention_dates)

            while current_date <= max_date:
                date_string = current_date.strftime("%Y-%m-%d")

                if date_string not in date_set:
                    intervention_dates.append(date_string)
                
                    caught_overalls.append(None)
                
                    titles.append("N/A")
                
                    status_types.append("N/A")
                
                    volunteer_amounts.append(None)
                
                current_date += timedelta(days = 1)

            sorted_data = sorted(zip(intervention_dates, caught_overalls, titles, status_types, volunteer_amounts))

            intervention_dates, caught_overalls, titles, status_types, volunteer_amounts = zip(*sorted_data)

            for item in range(len(intervention_dates)):
                data.append({"location": f"{location.barangay}, {location.municipality}", "municipality": location.municipality, "intervention_date": intervention_dates[item], "caught_amount": caught_overalls[item], "title": titles[item], "status_type": status_types[item], "volunteer_amount": volunteer_amounts[item]})

    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "chart_data": json.dumps(data), "locations": locations, "municipalities": municipalities, "barangays": barangays, "total_caught_overall": total_caught_overall, "selected_municipality": municipality_filter, "selected_barangay": barangay_filter, "year_filter": year_filter, "current_year": timezone.now().year, "status_data": status_data}

    return render(request, "officer/control/home/home.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlProfile(request):
    user = User.objects.get(account = request.user)

    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days=30)
    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by('-creation_date')[:5]

    context = {"user": user, "username": username, "user_profile": user_profile, "unread_notifications": unread_notifications}

    return render(request, "officer/control/profile/profile.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlProfileUpdate(request):
    user = User.objects.get(account = request.user)

    username = request.user.username

    user_profile = User.objects.get(account = request.user)


    notification_life = timezone.now() - timedelta(days=30)
    
    unread_notifications = Post.objects.filter(read_status=False, creation_date__gte=notification_life).order_by('-creation_date')[:5]
    
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance = request.user.user)
        
        if profile_form.is_valid():
            profile_form.save()

            username = request.user.username

            messages.success(request, username + ", " + "your information input was recorded online for COTSEye.")
            
    else:
        profile_form = ProfileForm(request.user.user)

    context = {"user": user, "username": username, "user_profile": user_profile, "profile_form": profile_form, "unread_notifications": unread_notifications}
    
    return render(request, "officer/control/profile/update.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlStatistics(request):
    username = request.user.username

    posts = Post.objects.all()

    posts_count = Post.objects.count()

    try:
        post_date = Post.objects.latest("capture_date").capture_date
        
    except:
        post_date = None

    statuses = Status.objects.all()
        
    statuses_count = Status.objects.count()

    try:
        status_date = Status.objects.latest("onset_date").onset_date
        
    except:
        status_date = None

    interventions = Intervention.objects.all()

    interventions_count = Intervention.objects.count()

    try:
        intervention_date = Intervention.objects.latest("intervention_date").intervention_date
        
    except:
        intervention_date = None
    
    context = {"username": username, "posts": posts, "posts_count": posts_count, "post_date": post_date, "statuses": statuses, "statuses_count": statuses_count, "status_date": status_date, "interventions": interventions, "interventions_count": interventions_count, "intervention_date": intervention_date, }

    return render(request, "officer/control/statistics/statistics.html", context)


@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlLogout(request):
    username = request.user.username

    logout(request)
    
    messages.success(request, username + ", " + "your account used just now was signed out of COTSEye.")
    
    return redirect("Officer Control Login")


def AdministratorControlLogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 1:
                login(request, account)
                
                return redirect("admin:index")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "admin/control/login/login.html", context)


def AdministratorCheck(account):
    try:
        return account.is_authenticated and account.usertype_id == 1 != None
    
    except Account.DoesNotExist:
            return False


@login_required(login_url = "admin:Administrator Control Login")
@user_passes_test(AdministratorCheck, login_url = "admin:Administrator Control Login")
def AdministratorControlLogout(request):    
    username = request.user.username

    logout(request)
        
    messages.success(request, username + ", " + "your account used just now was signed out of COTSEye.")
        
    return redirect("admin:Administrator Control Login")


def ControlHomeRedirect(request):
    usertype = request.user.usertype_id

    if usertype == 2:
        return redirect(reverse("index"))
    
    elif usertype == 1:
        return redirect(reverse("admin:index"))


def ControlPasswordRedirect(request):
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 2:
            return redirect(reverse("password_change"))
        
        elif usertype == 1:
            return redirect(reverse("admin:password_change"))
    
    else:
        return redirect(reverse("password_change"))


def ControlProfileRedirect(request):
    object = Account.objects.get(id = request.user.id)

    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 2:
            return redirect(reverse("authentications_account_change", kwargs = {"object_id": object.id}))

        elif usertype == 1:
            return redirect(reverse("admin:authentications_account_change", kwargs = {"object_id": object.id}))
    
    else:
        return redirect(reverse("authentications_account_change", kwargs = {"object_id": object.id}))
    

@login_required(login_url = "Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "Officer Control Login")
def OfficerControlNotification(request):
    unread_notifications_list = Post.objects.filter(read_status = False).order_by("-creation_date")[:5]

    now = timezone.now()
    read_posts_list = Post.objects.filter(read_status = True).filter(read_date__gte = now - timedelta(days = 30), read_date__lte = now).order_by("-creation_date")
    
    unread_paginator = Paginator(unread_notifications_list, 10) 

    read_paginator = Paginator(read_posts_list, 10)
    
    unread_page_number = request.GET.get("unread_page")

    read_page_number = request.GET.get("read_page")
    
    unread_notifications = unread_paginator.get_page(unread_page_number)

    read_posts = read_paginator.get_page(read_page_number)
    
    context = {"unread_notifications": unread_notifications, "read_posts": read_posts}
    
    return render(request, 'officer/control/notification/notification.html', context)