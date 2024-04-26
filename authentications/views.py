from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.socialaccount.signals import social_account_updated
from authentications.forms import AccountForm, UserForm, ProfileForm
from authentications.models import *
from auxiliaries.models import Announcement
from managements.models import Status, Intervention
from reports.models import Post

import base64
import json


# Create your views here.
def PublicServiceHome(request):
    user = request.user

    username = "public/everyone"

    latest_announcements = Announcement.objects.all().order_by("-release_date")[:3]

    latest_interventions = Intervention.objects.all().order_by("-intervention_date")[:3]

    valid_posts = Post.objects.filter(post_status = 1).order_by("-capture_date")[:3]

    if user.is_authenticated:
        if user.usertype_id == 3:
            return redirect("Contributor Service Home")
        
        elif user.usertype_id == 2:
            return redirect("officer:index")
        
        elif user.usertype_id == 1:
            return redirect("admin:index")

    else:
        if not any(message.level in [messages.INFO, messages.SUCCESS, messages.ERROR] for message in messages.get_messages(request)):
            messages.info(request, username + ", " + "kindly see announcements within COTSEye to check for updates today.")

    context = {"username": username, "latest_announcements": latest_announcements, "latest_interventions": latest_interventions, "valid_posts": valid_posts}
    
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
                        
                        username = "google/" + email.split("@")[0]
                        
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
                       
                        username = "facebook/" + email.split("@")[0]
                        
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

    latest_announcements = Announcement.objects.all().order_by("-release_date")[:3]

    latest_interventions = Intervention.objects.all().order_by("-intervention_date")[:3]

    valid_posts = Post.objects.filter(post_status = 1).order_by("-capture_date")[:3]
    
    context = {"username": username, "latest_announcements": latest_announcements, "latest_interventions": latest_interventions, "valid_posts": valid_posts}

    return render(request, "contributor/service/home/home.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceProfile(request):
    user = User.objects.get(account = request.user)

    username = request.user.username

    context = {"user": user, "username": username}

    return render(request, "contributor/service/profile/profile.html", context)


@login_required(login_url = "Contributor Service Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Service Login")
def ContributorServiceProfileUpdate(request):
    user = User.objects.get(account = request.user)

    username = request.user.username

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance = request.user.user)
        
        if profile_form.is_valid():
            profile_form.save()

            username = request.user.username

            messages.success(request, username + ", " + "your information input was recorded online for COTSEye.")
            
            return redirect("Contributor Service Profile")
            
    else:
        profile_form = ProfileForm(request.user.user)

    context = {"user": user, "username": username, "profile_form": profile_form}
    
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

    fallback = "The COTSEye cannot keep in touch to the requested page today, as such is not found within the cache storage."

    context = {"contributor": contributor, "fallback": fallback}
    
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
                
                return redirect("officer:Officer Control Login")
        
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
                
                return redirect("officer:Officer Control Login")
            
            else:
                if sociallogin.account.provider == "google":
                    user = sociallogin.user
                    
                    user.usertype_id = 2

                    if "email" in sociallogin.account.extra_data:
                        email = sociallogin.account.extra_data["email"]
                        
                        username = "google/" + email.split("@")[0]
                        
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
                
                return redirect("officer:Officer Control Login")
            
            else:
                if sociallogin.account.provider == "facebook":
                    user = sociallogin.user
                    
                    user.usertype_id = 2

                    if "email" in sociallogin.account.extra_data:
                        email = sociallogin.account.extra_data["email"]
                        
                        username = "facebook/" + email.split("@")[0]
                        
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
                
                return redirect("officer:index")
            
            else:
                messages.error(request, "Username or password is not valid.")

        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "officer/control/login/login.html", context)


def OfficerControlLoginFacebook(request):
    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 2:
                login(request, account)
                
                return redirect("officer:index")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}
    
    return render(request, "officer/control/login/facebook.html", context)


def OfficerControlLoginGoogle(request):
    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 2:
                login(request, account)
                
                return redirect("officer:index")
            
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
    

@login_required(login_url = "officer:Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "officer:Officer Control Login")
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
    
    context = {"username": username, "posts": posts, "posts_count": posts_count, "post_date": post_date, "statuses": statuses, "statuses_count": statuses_count, "status_date": status_date, "interventions": interventions, "interventions_count": interventions_count, "intervention_date": intervention_date}

    return render(request, "officer/control/statistics/statistics.html", context)


@login_required(login_url = "officer:Officer Control Login")
@user_passes_test(OfficerCheck, login_url = "officer:Officer Control Login")
def OfficerControlLogout(request):
    username = request.user.username

    logout(request)
    
    messages.success(request, username + ", " + "your account used just now was signed out of COTSEye.")
    
    return redirect("officer:Officer Control Login")


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
def AdministratorControlStatistics(request):
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
    
    context = {"username": username, "posts": posts, "posts_count": posts_count, "post_date": post_date, "statuses": statuses, "statuses_count": statuses_count, "status_date": status_date, "interventions": interventions, "interventions_count": interventions_count, "intervention_date": intervention_date}
    
    return render(request, "admin/control/statistics/statistics.html", context)


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
        return redirect(reverse("officer:index"))
    
    elif usertype == 1:
        return redirect(reverse("admin:index"))


def ControlPasswordRedirect(request):
    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 2:
            return redirect(reverse("officer:password_change"))
        
        elif usertype == 1:
            return redirect(reverse("admin:password_change"))
    
    else:
        return redirect(reverse("officer:password_change"))

def ControlProfileRedirect(request):
    object = Account.objects.get(id = request.user.id)

    if request.user.is_authenticated:
        usertype = request.user.usertype_id

        if usertype == 2:
            return redirect(reverse("officer:authentications_account_change", kwargs = {"object_id": object.id}))

        elif usertype == 1:
            return redirect(reverse("admin:authentications_account_change", kwargs = {"object_id": object.id}))
    
    else:
        return redirect(reverse("officer:authentications_account_change", kwargs = {"object_id": object.id}))