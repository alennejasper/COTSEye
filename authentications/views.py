from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db.models import Max
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from allauth.socialaccount.signals import pre_social_login
from authentications.forms import AccountForm, UserForm, ProfileForm
from authentications.models import *
from managements.models import Status, Announcement, Activity, Location, Municipality, Barangay
from reports.models import Post
from django.db.models import Count
from operator import itemgetter
from allauth.socialaccount.models import SocialAccount

import base64
import json


# Create your views here.
def PublicServiceFallback(request):
    public = "public/anyone"

    fallback = "You are currently offline and the requested page is not available. Kindly check your connection and try again."

    context = {"public": public, "fallback": fallback}
    
    return render(request, "public/service/fallback/fallback.html", context)


def PublicServiceHome(request):
    user = request.user

    username = "public/anyone"

    latest_announcements = Announcement.objects.all().order_by("-event_date")[:3]

    valid_posts = Post.objects.filter(post_status = 1).order_by("-capture_date")[:3]

    if user.is_authenticated:
        if user.usertype_id == 3:
            logout(request)

            username = user.username
        
            messages.success(request, username + ", " + "you have successfully logged out. Have a great day ahead!")

            return redirect("Public Service Home")
        
        elif user.usertype_id == 2:
            logout(request)
        
            username = user.username

            messages.success(request, username + ", " + "you have successfully logged out. Have a great day ahead!")

            return redirect("Public Service Home")
        
        elif user.usertype_id == 1:
            logout(request)

            username = user.username

            messages.success(request, username + ", " + "you have successfully logged out. Have a great day ahead!")

            return redirect("Public Service Home")

    else:
        try:
            map_posts = Post.objects.filter(post_status = 1)

            map_statuses = Status.objects.all()

            six_months_ago = timezone.now() - timedelta(days = 180)

            map_posts = Post.objects.filter(post_status = 1, creation_date__gte = six_months_ago)

            map_statuses = Status.objects.filter(creation_date__gte = six_months_ago)

        except:
            map_posts = None

            map_statuses = None

    context = {"username": username, "map_posts": map_posts, "map_statuses": map_statuses, "latest_announcements": latest_announcements, "valid_posts": valid_posts}
    
    return render(request, "public/service/home/home.html", context)


def ContributorServiceFallback(request):
    contributor = "contributor/anyone"

    fallback = "You are currently offline and the requested page is not available. Kindly check your connection and try again."

    context = {"contributor": contributor, "fallback": fallback}
    
    return render(request, "contributor/service/fallback/fallback.html", context)


def ContributorServiceRegister(request):
    username = "public/anyone"

    account_form = AccountForm()

    user_form = UserForm()

    if request.method == "POST":
        account_form = AccountForm(request.POST)

        user_form = UserForm(request.POST)

        if account_form.is_valid() and user_form.is_valid():
            account = account_form.save(commit = False)

            user = user_form.save(commit = False)

            usertype = UserType.objects.get(id = 3)

            active = True

            account = Account.objects.create(username = account.username, password = account.password, usertype = usertype, is_active = active)
            
            if Account.objects.filter(username = account.username, password = account.password, usertype = usertype, is_active = active).exists():
                User.objects.create(account = account, first_name = user.first_name, last_name = user.last_name, email = user.email, phone_number = user.phone_number)
                
                username = account.username
                
                messages.success(request, username + ", " + "your account has been successfully registered. Kindly proceed to log in with your credentials.")
                
                return redirect("Contributor Service Login")
        
        else:            
            for field, errors in account_form.errors.items():
                messages.error(request, "There is an issue in the" + " " + field + " field." + " " + ", ".join(errors))

            for field, errors in user_form.errors.items():
                messages.error(request, "There is an issue in the" + " " + field + " field." + " " + ", ".join(errors))

    else:
        account_form = AccountForm()
        
        user_form = UserForm()

    context = {"username": username, "account_form": account_form, "user_form": user_form}
    
    return render(request, "contributor/service/register/register.html", context)


def ContributorServiceLogin(request):
    @receiver(pre_social_login)
    def UpdateUser(sender, request, sociallogin, **kwargs):
        if not request or not hasattr(request, "is_contributor"):
            return
    
        elif sociallogin.account.provider == "google":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 2:
                messages.error(request, "Account not found. Kindly create a new one and try again.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Contributor Service Login")

            elif sociallogin.user.is_active == False:
                messages.error(request, "Account is not active. Kindly contact support for assistance.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Contributor Service Login")
            
            else:
                if sociallogin.account.provider == "google":     
                    user = sociallogin.user

                    user.usertype_id = 3

                    user.is_active = True
                    
                    email = sociallogin.account.extra_data["email"]

                    username = email.split("@")[0]
                    
                    user.save()

                    sociallogin.account.user = user

                    sociallogin.account.save()

                    instance, created = User.objects.get_or_create(account = user)

                    if created:
                        instance.account.username = username

                        instance.email = email

                        instance.first_name = sociallogin.account.extra_data.get("given_name", "")

                        instance.last_name = sociallogin.account.extra_data.get("family_name", "")
                        
                        instance.save()

                    else:
                        pass
                
        elif sociallogin.account.provider == "facebook":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 2:
                messages.error(request, "Account not found. Kindly create a new one and try again.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Contributor Service Login")
            
            elif sociallogin.user.is_active == False:
                messages.error(request, "Account is not active. Kindly contact support for assistance.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Contributor Service Login")
            
            else:
                if sociallogin.account.provider == "facebook": 
                    user = sociallogin.user
                   
                    user.usertype_id = 3

                    user.is_active = True
                    
                    email = sociallogin.account.extra_data["email"]

                    username = email.split("@")[0]
                    
                    user.save()

                    user = sociallogin.account.user

                    sociallogin.account.save()

                    sociallogin.account.user = user

                    instance, created = User.objects.get_or_create(account = user)

                    if created:
                        instance.account.username = username

                        instance.email = email

                        instance.first_name = sociallogin.account.extra_data.get("given_name", "")

                        instance.last_name = sociallogin.account.extra_data.get("family_name", "")

                        instance.save()

                    else:
                        pass
                        
    pre_social_login.connect(UpdateUser, sender = None)
     
    request.is_contributor = True

    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")

        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 3:
                login(request, account)
                
                return redirect("Contributor Service Home")
            
            else:
                messages.error(request, "Account not found. Kindly create a new one and try again.")
        
        else:
            messages.error(request, "Account not found. Kindly create a new one and try again.")
    
    user = request.user

    if user.is_authenticated:
        if user.usertype_id == 2:
            logout(request)
        
            username = user.username

            messages.info(request, username + ", " + "you need authorization to proceed. Kindly contact support for assistance.")

            return redirect("Contributor Service Login")
        
        elif user.usertype_id == 1:
            logout(request)

            username = user.username

            messages.info(request, username + ", " + "you need authorization to proceed. Kindly contact support for assistance.")

            return redirect("Contributor Service Login")

    context = {}

    return render(request, "contributor/service/login/login.html", context)


def ContributorCheck(account):
    try:
        return account.is_authenticated and account.usertype_id == 3 != None
    
    except Account.DoesNotExist:
            return False

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceLeaderboard(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    valid_posts = Post.objects.filter(post_status__is_valid = True)
    
    leaderboard = valid_posts.values("user__account__username", "user__profile_photo").annotate(post_count = Count("id")).order_by('-post_count')

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    context = {"leaderboard": leaderboard, "username": username, "user_profile": user_profile, "valid_posts": valid_posts, "unread_notifications": unread_notifications,}

    return render(request, "contributor/service/leaderboard/leaderboard.html", context)

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceHome(request):
    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)
        
    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    latest_announcements = Announcement.objects.all().order_by("-event_date")[:3]

    valid_posts = Post.objects.filter(post_status = 1).order_by("-capture_date")[:3]
            
    try:
        map_posts = Post.objects.filter(post_status = 1)

        map_statuses = Status.objects.all()

        six_months_ago = timezone.now() - timedelta(days = 180)

        map_posts = Post.objects.filter(post_status = 1, creation_date__gte = six_months_ago)

        map_statuses = Status.objects.filter(creation_date__gte = six_months_ago)

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

    user = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")
   
    notification_items = Notification.objects.filter(user = user, creation_date__gte = notification_life).order_by("-creation_date")
            
    context = {"username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "notification_items": notification_items}
    
    return render(request, "contributor/service/notification/notification.html", context)


def ContributorServiceNotificationMark(request, id):
    try:
        post = Post.objects.get(id = id)

        post.contrib_read_status = True

        post.contrib_read_date = timezone.now()

        post.save()

        return redirect("Contributor Service Notification") 
    
    except Post.DoesNotExist:
        return JsonResponse({"success": False, "error": "The post could not be found. Kindly try again later."})
    

def ContributorServiceMarkNotificationAsRead(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(account = request.user)

        notification = get_object_or_404(Notification, id = id, user = user)

        notification.is_read = True

        notification.save()

        if notification.contenttype.model == "post":
            return redirect("Contributor Service Post Read", id = notification.key)
        
        elif notification.contenttype.model == "announcement":
            return redirect("Contributor Service Announcement Read", id = notification.key)
        
        elif notification.contenttype.model == "activity":
            return redirect("Contributor Service Activity Read", id = notification.key)
        
        elif notification.notificationtype  == "achievement":
            return redirect("Contributor Service Profile")
        
        else:
            return redirect("Contributor Service Notification")
        
    else:
        return redirect("Contributor Service Login")
    

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceProfile(request):
    user = User.objects.get(account = request.user)

    username = request.user.username

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    user_profile = User.objects.get(account = request.user)

    user_sightings = Post.objects.filter(user = user_profile, post_status = 1).count()

    context = {"user": user, "username": username, "unread_notifications": unread_notifications, "user_profile": user_profile, "user_sightings": user_sightings}

    return render(request, "contributor/service/profile/profile.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceProfileUpdate(request):
    user = User.objects.get(account = request.user)

    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    user = User.objects.get(account = request.user)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance = request.user.user)
        
        if profile_form.is_valid():
            profile_form.save()

            username = request.user.username

            messages.success(request, username + ", " + "your profile has been successfully updated.")
            
            return redirect("Contributor Service Profile")
        
        else:
            for field, errors in profile_form.errors.items():
                messages.error(request, "Error in" + " " + field + " field." + " " + ", ".join(errors))
            
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
                

@login_required(login_url = "Contributor Control Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Control Login")
def ContributorServiceProfileDelete(request, id):
    account = Account.objects.get(id = id)

    account.is_active = False

    account.save()

    user = User.objects.get(account = id)

    administrators = User.objects.filter(account__usertype_id = 1)

    for administrator in administrators:
        subject = "COTSEye has delivered an alert message!"

        scheme = request.scheme

        host = request.META["HTTP_HOST"]

        template = render_to_string("contributor/service/profile/email.html", {"administrator": administrator.account.username, "contributor": user.account.username, "account": account, "scheme": scheme, "host": host})

        body = strip_tags(template)

        source = "COTSEye <settings.EMAIL_HOST_USER>"

        recipient = [administrator.email]

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

    messages.success(request, username + ", " + "your account has been deactivated successfully.")

    return redirect("Public Service Home")

@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceProfileDeleteFetch(request):
    if request.method == "POST":
        information = json.loads(request.body)

    for information in information:
        account = information.get("account")

        account = Account.objects.get(id = account)

        account.is_active = False

        account.save()
    
        user = User.objects.get(account = account)

        administrators = User.objects.filter(account__usertype_id = 1)

        for administrator in administrators:
            subject = "COTSEye has delivered an alert message!"

            scheme = request.scheme

            host = request.META["HTTP_HOST"]

            template = render_to_string("contributor/service/profile/email.html", {"administrator": administrator.account.username, "contributor": user.account.username, "account": account, "scheme": scheme, "host": host})

            body = strip_tags(template)

            source = "COTSEye <settings.EMAIL_HOST_USER>"

            recipient = [administrator.email]

            email = EmailMultiAlternatives(
                subject,
                
                body,
                
                source,
                
                recipient,
            )

            email.attach_alternative(template, "text/html")

            email.fail_silently = False

            email.send()


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceLogout(request):
    username = request.user.username

    logout(request)
    
    messages.success(request, username + ", " + "you have successfully logged out. Have a great day ahead!")
    
    return redirect("Public Service Home")


def CuratorControlFallback(request):
    curator = "curator/anyone"

    fallback = "Your device screen is too small to view this page. Please try again on a device with a screen width of 1080px or higher."

    context = {"curator": curator, "fallback": fallback}
    
    return render(request, "curator/control/fallback/fallback.html", context)


def CuratorControlRegister(request):
    username = "public/anyone"

    account_form = AccountForm()

    user_form = UserForm()

    if request.method == "POST":
        account_form = AccountForm(request.POST)

        user_form = UserForm(request.POST)

        if account_form.is_valid() and user_form.is_valid():
            account = account_form.save(commit = False)

            user = user_form.save(commit = False)

            usertype = UserType.objects.get(id = 2)

            inactive = False

            account = Account.objects.create(username = account.username, password = account.password, usertype = usertype, is_active = inactive)
            
            if Account.objects.filter(username = account.username, password = account.password, usertype = usertype, is_active = inactive).exists():
                curator = User.objects.create(account = account, first_name = user.first_name, last_name = user.last_name, email = user.email, phone_number = user.phone_number)
                
                administrators = User.objects.filter(account__usertype_id = 1)

                for administrator in administrators:
                    subject = "COTSEye has delivered an alert message!"

                    scheme = request.scheme

                    host = request.META["HTTP_HOST"]

                    template = render_to_string("curator/control/register/email.html", {"administrator": administrator.account.username, "curator": curator.account.username, "account": account, "scheme": scheme, "host": host})

                    body = strip_tags(template)

                    source = "COTSEye <settings.EMAIL_HOST_USER>"

                    recipient = [administrator.email]

                    email = EmailMultiAlternatives(
                        subject,
                        
                        body,
                        
                        source,
                        
                        recipient,
                    )

                    email.attach_alternative(template, "text/html")

                    email.fail_silently = False

                    email.send()

                username = account.username
                
                messages.success(request, username + ", " + "your account has been successfully registered. Kindly wait for an email approval from the administrator.")
                
                return redirect("Curator Control Login")
        
        else:
            for field, errors in account_form.errors.items():
                messages.error(request, "There is an issue in the" + " " + field + " field." + " " + ", ".join(errors))

            for field, errors in user_form.errors.items():
                messages.error(request, "There is an issue in the" + " " + field + " field." + " " + ", ".join(errors))  

    else:
        account_form = AccountForm()
        
        user_form = UserForm()

    context = {"username": username, "account_form": account_form, "user_form": user_form}
    
    return render(request, "curator/control/register/register.html", context)


def CuratorControlLogin(request):
    @receiver(pre_social_login)
    def UpdateUser(sender, request, sociallogin, **kwargs):
        if not request or not hasattr(request, "is_staff"):
            return
        
        elif sociallogin.account.provider == "google":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 3:
                messages.error(request, "Account not found. Kindly create a new one and try again.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Curator Control Login")

            elif sociallogin.user.is_active == False:
                messages.error(request, "Account is not active. Kindly contact support for assistance.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Curator Control Login")
            
            else:
                if sociallogin.account.provider == "google":
                    user = sociallogin.user
                   
                    user.usertype_id = 2

                    user.is_active = False
                    
                    email = sociallogin.account.extra_data["email"]

                    username = email.split("@")[0]
                    
                    user.save()

                    sociallogin.account.user = user

                    sociallogin.account.save()

                    instance, created = User.objects.get_or_create(account = user)

                    if created:
                        instance.account.username = username

                        instance.email = email

                        instance.first_name = sociallogin.account.extra_data.get("given_name", "")

                        instance.last_name = sociallogin.account.extra_data.get("family_name", "")
                        
                        instance.save()

                    else:
                        pass
        
        elif sociallogin.account.provider == "facebook":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 3:
                messages.error(request, "Account not found. Kindly create a new one and try again.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Curator Control Login")
            
            elif sociallogin.user.is_active == False:
                messages.error(request, "Account is not active. Kindly contact support for assistance.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Curator Control Login")
            
            else:
                if sociallogin.account.provider == "facebook":                  
                    user = sociallogin.user
                   
                    user.usertype_id = 2

                    user.is_active = False
                    
                    email = sociallogin.account.extra_data["email"]

                    username = email.split("@")[0]
                    
                    user.save()

                    sociallogin.account.user = user

                    sociallogin.account.save()

                    instance, created = User.objects.get_or_create(account = user)

                    if created:
                        instance.account.username = username
                        
                        instance.email = email

                        instance.first_name = sociallogin.account.extra_data.get("given_name", "")

                        instance.last_name = sociallogin.account.extra_data.get("family_name", "")
                        
                        instance.save()

                    else:
                        pass
    
    pre_social_login.connect(UpdateUser, sender = None)

    request.is_staff = True
    
    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")

        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 2:
                login(request, account)
                
                return redirect("Curator Control Home")

            else:
                messages.error(request, "Account not found. Kindly create a new one and try again.")
        
        else:
            messages.error(request, "Account not found. Kindly create a new one and try again.")

    user = request.user

    if user.is_authenticated:
        if user.usertype_id == 3:
            logout(request)
        
            username = user.username

            messages.info(request, username + ", " + "you need authorization to proceed. Kindly contact support for assistance.")

            return redirect("Curator Control Login")
        
        elif user.usertype_id == 1:
            logout(request)

            username = user.username

            messages.info(request, username + ", " + "you need authorization to proceed. Kindly contact support for assistance.")

            return redirect("Curator Control Login")
        
    context = {}

    return render(request, "curator/control/login/login.html", context)


def CuratorCheck(account):
    try:
        return account.is_authenticated and account.usertype_id == 2 != None
    
    except Account.DoesNotExist:
            return False
    

@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlHome(request):
    tab_number = 1

    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    valid_posts = Post.objects.filter(post_status__is_valid = True)

    leaderboard = valid_posts.values("user__account__username").annotate(post_count = Count("id")).order_by("-post_count")

    user = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    municipality_filter = request.GET.get("municipality")

    barangay_filter = request.GET.get("barangay")

    year_filter = request.GET.get("year")

    latest_statuses = Status.objects.values("location__municipality").annotate(max_date = Max("onset_date"))

    latest_status_entries = Status.objects.filter(location__municipality__in = [status["location__municipality"] for status in latest_statuses], onset_date__in = [status["max_date"] for status in latest_statuses]).order_by("location__municipality").distinct("location__municipality")
   
    status_data = []

    for status_entry in latest_status_entries:
        status_data.append({"municipality": status_entry.location.municipality.municipality_name, "caught_amount": status_entry.caught_overall, "volunteer_amount": status_entry.volunteer_overall, "status_type": str(status_entry.statustype.statustype), "activity_date": status_entry.onset_date.strftime("%m/%d/%Y")})
    
    status_order = {"Critical": 1, "High": 2, "Moderate": 3, "Low": 4, "None": 5}

    status_data = sorted(status_data, key = lambda x: status_order.get(x["status_type"], float("inf")))

    municipalities = Municipality.objects.values("municipality_name").distinct()

    barangays = Barangay.objects.values("barangay_name").distinct()

    if municipality_filter:
        barangays = Barangay.objects.filter(municipality__municipality_name=municipality_filter).values("barangay_name").distinct()

    locations_query = Location.objects.all()

    if municipality_filter:
        locations_query = locations_query.filter(municipality__municipality_name = municipality_filter)

    else:
        municipality_filter = "Alabel"

        locations_query = locations_query.filter(municipality__municipality_name = municipality_filter)

    if barangay_filter:
        locations_query = locations_query.filter(barangay__barangay_name = barangay_filter)

    else:
        barangay_filter = "Kawas"

        locations_query = locations_query.filter(barangay__barangay_name = barangay_filter)

    locations = locations_query.distinct()

    data = []

    total_caught_overall = 0

    for location in locations:
        activities_query = Activity.objects.filter(location = location).order_by("activity_date")
        
        if year_filter:
            start_date = datetime.datetime.strptime(year_filter, "%Y").replace(month = 1, day = 1)

            end_date = datetime.datetime.strptime(year_filter, "%Y").replace(month = 12, day = 31)

            activities_query = activities_query.filter(activity_date__range = [start_date, end_date])

        else:
            start_date = datetime.datetime.strptime("2024", "%Y").replace(month = 1, day = 1)

            end_date = datetime.datetime.strptime("2024", "%Y").replace(month = 12, day = 31)

            activities_query = activities_query.filter(activity_date__range = [start_date, end_date])

        activity_dates = []

        caught_overalls = []
        
        titles = []
        
        status_types = []
        
        volunteer_amounts = []
        
        caught_overall_sum = 0

        for activity in activities_query:
            if activity.statustype:
                activity_dates.append(activity.activity_date.strftime("%Y-%m-%d"))

                caught_overalls.append(activity.caught_amount)
                
                titles.append(activity.title)
                
                status_types.append(str(activity.statustype))
                
                volunteer_amounts.append(activity.volunteer_amount)
                
                caught_overall_sum += activity.caught_amount

        total_caught_overall += caught_overall_sum

        if activity_dates:
            min_date = datetime.datetime.strptime(activity_dates[0], "%Y-%m-%d")

            max_date = datetime.datetime.strptime(activity_dates[-1], "%Y-%m-%d")
            
            current_date = min_date
            
            date_set = set(activity_dates)

            while current_date <= max_date:
                date_string = current_date.strftime("%Y-%m-%d")

                if date_string not in date_set:
                    activity_dates.append(date_string)
                
                    caught_overalls.append(None)
                
                    titles.append("N/A")
                
                    status_types.append("N/A")
                
                    volunteer_amounts.append(None)
                
                current_date += timedelta(days = 1)

            sorted_data = sorted(zip(activity_dates, caught_overalls, titles, status_types, volunteer_amounts))

            activity_dates, caught_overalls, titles, status_types, volunteer_amounts = zip(*sorted_data)

            for item in range(len(activity_dates)):
                data.append({"location": f"{location.barangay.barangay_name}, {location.municipality.municipality_name}", "municipality": location.municipality.municipality_name, "activity_date": activity_dates[item], "caught_amount": caught_overalls[item], "title": titles[item], "status_type": status_types[item], "volunteer_amount": volunteer_amounts[item]})

    context = {"leaderboard": leaderboard, "tab_number": tab_number, "username": username, "user_profile": user_profile, "unread_notifications": unread_notifications, "chart_data": json.dumps(data), "locations": locations, "municipalities": municipalities, "barangays": barangays, "total_caught_overall": total_caught_overall, "selected_municipality": municipality_filter, "selected_barangay": barangay_filter, "year_filter": year_filter, "current_year": timezone.now().year, "status_data": status_data}

    return render(request, "curator/control/home/home.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlNotification(request):
    tab_number = 6 

    notification_number = 1

    user = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    unread_notifications_list = Notification.objects.filter(notificationtype = "post", user = user, is_read = False).order_by("-creation_date")

    read_posts_list  = Notification.objects.filter(notificationtype = "post", user = user, is_read = True).order_by("-creation_date")
    
    unread_paginator = Paginator(unread_notifications_list, 10) 

    read_paginator = Paginator(read_posts_list, 10)
    
    unread_page_number = request.GET.get("unread_page")

    read_page_number = request.GET.get("read_page")
    
    unread_posts = unread_paginator.get_page(unread_page_number)

    read_posts = read_paginator.get_page(read_page_number)
    
    context = {"tab_number": tab_number, "notification_number": notification_number, "unread_notifications": unread_notifications, "unread_posts": unread_posts, "read_posts": read_posts}
    
    return render(request, "curator/control/notification/notification.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlNotificationMark(request, id):
    post = Post.objects.get(id = id)

    post.read_status = True

    post.read_date = timezone.now()

    if request.user.usertype.id == 2:
        post.validator = request.user.user
        
    post.save()

    return redirect("Curator Control Notification")


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlNotificationRead(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(account = request.user)

        notification = get_object_or_404(Notification, id = id, user = user)

        notification.is_read = True

        notification.save()

        if notification.contenttype.model == "post":
            return redirect("Curator Control Sighting Read", id = notification.key)
        
        else:
            return redirect("Curator Control Notification")
        
    else:
        return redirect("Curator Control Login")
    
    
@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlProfile(request):
    tab_number = 7 

    profile_number = 1

    account = Account.objects.get(id = request.user.id)

    user = User.objects.get(account = request.user)

    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)

    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]

    context = {"tab_number": tab_number, "profile_number": profile_number, "account": account, "user": user, "username": username, "user_profile": user_profile, "unread_notifications": unread_notifications}

    return render(request, "curator/control/profile/profile.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlProfileUpdate(request):
    profile_number = 2

    user = User.objects.get(account = request.user)

    username = request.user.username

    user_profile = User.objects.get(account = request.user)

    notification_life = timezone.now() - timedelta(days = 30)
    
    unread_notifications = Notification.objects.filter(user = user, is_read = False, creation_date__gte = notification_life).order_by("-creation_date")[:3]
    
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance = request.user.user)
        
        if profile_form.is_valid():
            profile_form.save()

            username = request.user.username

            messages.success(request, username + ", " + "your information input was recorded online for COTSEye.")

            return redirect("Curator Control Profile")
        
        else:
            for field, errors in profile_form.errors.items():
                messages.error(request, "Error in" + " " + field + " field." + " " + ", ".join(errors))
            
    else:
        profile_form = ProfileForm(request.user.user)

    context = {"profile_number": profile_number, "user": user, "username": username, "user_profile": user_profile, "profile_form": profile_form, "unread_notifications": unread_notifications}
    
    return render(request, "curator/control/profile/update.html", context)


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlProfileDelete(request, id):
    account = Account.objects.get(id = id)

    account.is_active = False

    account.save()

    user = User.objects.get(account = id)

    administrators = User.objects.filter(account__usertype_id = 1)

    for administrator in administrators:
        subject = "COTSEye has delivered an alert message!"

        scheme = request.scheme

        host = request.META["HTTP_HOST"]

        template = render_to_string("curator/control/profile/email.html", {"administrator": administrator.account.username, "curator": user.account.username, "account": account, "scheme": scheme, "host": host})

        body = strip_tags(template)

        source = "COTSEye <settings.EMAIL_HOST_USER>"

        recipient = [administrator.email]

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

    messages.success(request, username + ", " + "your account was deactivated online from COTSEye.")

    return redirect("Curator Control Login")


@login_required(login_url = "Curator Control Login")
@user_passes_test(CuratorCheck, login_url = "Curator Control Login")
def CuratorControlLogout(request):
    username = request.user.username

    logout(request)
    
    messages.success(request, username + ", " + "you have successfully logged out. Have a great day ahead!")
    
    return redirect("Curator Control Login")


def AdministratorControlFallback(request):
    administrator = "administrator"

    fallback = "Your device screen is too small to view this page. Please try again on a device with a screen width of 1080px or higher."

    context = {"administrator": administrator, "fallback": fallback}
    
    return render(request, "admin/control/fallback/fallback.html", context)


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
                messages.error(request, "Account not found. Kindly create a new one and try again.")
        
        else:
            messages.error(request, "Account not found. Kindly create a new one and try again.")
    
    user = request.user

    if user.is_authenticated:
        if user.usertype_id == 3:
            logout(request)
        
            username = user.username

            messages.success(request, username + ", " + "you have successfully logged out. Have a great day ahead!")

            return redirect("admin:Administrator Control Login")
        
        elif user.usertype_id == 2:
            logout(request)

            username = user.username

            messages.success(request, username + ", " + "you have successfully logged out. Have a great day ahead!")

            return redirect("admin:Administrator Control Login")
        
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
        
    messages.success(request, username + ", " + "you have successfully logged out. Have a great day ahead!")
        
    return redirect("admin:Administrator Control Login")


def ControlProfileRedirect(request, id):
    object = Account.objects.get(id = id)
    
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 2:
            return redirect(reverse("admin:authentications_account_change", kwargs = {"object_id": object.id}))

        elif usertype == 1:
            return redirect(reverse("admin:authentications_account_change", kwargs = {"object_id": object.id}))
    
    else:
        return redirect(reverse("admin:authentications_account_change", kwargs = {"object_id": object.id}))


def ForgeryReadRedirect(request, reason = ""):
    if request.user.is_authenticated:
        user = "public/anyone"

    else:
        user = request.user.username

    forgery = "Your browser has invalid CSRF token. Kindly refresh the page and try again."

    context = {"reason": reason, "user": user, "forgery": forgery}

    return render(request, "webwares/forgery.html", context)