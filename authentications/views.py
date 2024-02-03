from django.shortcuts import render, redirect
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from allauth.socialaccount.signals import social_account_updated
from authentications.forms import AccountForm, UserForm, ProfileForm
from authentications.models import *
from reports.models import Post


# Create your views here.
def PublicHome(request):
    user = request.user

    username = "public/everyone"

    if user.is_authenticated:
        if user.usertype_id == 3:
            return redirect("Contributor Home")
        
        elif user.usertype_id == 2 or user.usertype_id == 1:
            return redirect("admin:index")
    
    else:
        try:
            posts = Post.objects.filter(id = 1)
    
        except:
            posts = None

    if not any(message.level in [messages.INFO, messages.SUCCESS, messages.ERROR] for message in messages.get_messages(request)):
        messages.info(request, username + ", " + "kindly see announcements within the menu of COTSEye to check for updates today.")

    context = {"posts": posts}
    
    return render(request, "public/home/home.html", context)


def ContributorRegister(request):
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
                
                messages.success(request, username + ", " + "your information input was recorded for COTSEye.")
                
                return redirect("Contributor Login")
        
        else:
            messages.error(request, "Username exists or is not valid, or passwords are short, entirely numeric, or do not match.")
            
            messages.error(request, account_form.errors, user_form.errors) 

    else:
        account_form = AccountForm()
        
        user_form = UserForm()

    context = {"account_form": account_form, "user_form": user_form}
    
    return render(request, "contributor/register/register.html", context)


def ContributorLogin(request):
    @receiver(social_account_updated)
    def UpdateUser(sender, request, sociallogin, **kwargs):
        if sociallogin.account.provider == "google":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 2:
                messages.error(request, "Username or password is not valid.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Contributor Login")
            
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
                
                return redirect("Contributor Login")
            
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
                
                return redirect("Contributor Home")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "contributor/login/login.html", context)


def ContributorLoginFacebook(request):
    if request.method == "POST":
        username = request.POST.get("username")

        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 3:
                login(request, account)

                return redirect("admin:index")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "contributor/login/facebook.html", context)


def ContributorLoginGoogle(request):
    if request.method == "POST":
        username = request.POST.get("username")

        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 3:
                login(request, account)

                return redirect("admin:index")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "contributor/login/google.html", context)


def ContributorCheck(account):
    try:
        return account.is_authenticated and account.usertype_id == 3 != None
    
    except Account.DoesNotExist:
            return False


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorHome(request):
    posts = Post.objects.filter(id = 1)

    context = {"posts": posts}

    return render(request, "contributor/home/home.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorProfile(request):
    user = User.objects.get(account = request.user)

    context = {"user": user}

    return render(request, "contributor/profile/profile.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorProfileUpdate(request):
    user = User.objects.get(account = request.user)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance = request.user.user)
        
        if profile_form.is_valid():
            profile_form.save()

            username = request.user.username

            messages.success(request, username + ", " + "your information input was recorded for COTSEye.")
            
            return redirect("Contributor Profile")
            
    else:
        profile_form = ProfileForm(request.user.user)

    context = {"user": user, "profile_form": profile_form}
    
    return render(request, "contributor/profile/update.html", context)


@login_required(login_url = "Contributor Login")
@user_passes_test(ContributorCheck, login_url = "Contributor Login")
def ContributorLogout(request):
    username = request.user.username

    logout(request)
    
    messages.success(request, username + ", " + "your account used just now was signed out of COTSEye.")
    
    return redirect("Public Home")


def OfficerRegister(request):
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
                
                messages.success(request, username + ", " + "your information input was recorded for COTSEye.")
                
                return redirect("Officer Login")
        
        else:
            messages.error(request, "Username exists or is not valid, or passwords are short, entirely numeric, or do not match.")
            
            messages.error(request, account_form.errors, user_form.errors)  

    else:
        account_form = AccountForm()
        
        user_form = UserForm()

    context = {"account_form": account_form, "user_form": user_form}
    
    return render(request, "officer/register/register.html", context)


def OfficerLogin(request):
    @receiver(social_account_updated)
    def UpdateUser(sender, request, sociallogin, **kwargs):
        if sociallogin.account.provider == "google":
            if sociallogin.user.usertype_id == 1 or sociallogin.user.usertype_id == 3:
                messages.error(request, "Username or password is not valid.")
                
                sociallogin.state["process"] = "disconnect"
                
                sociallogin.state["save"] = False
                
                return redirect("Officer Login")
            
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
                
                return redirect("Officer Login")
            
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
                
                return redirect("admin:index")
            
            else:
                messages.error(request, "Username or password is not valid.")

        else:
            messages.error(request, "Username or password is not valid.")

    context = {}

    return render(request, "officer/login/login.html", context)


def OfficerLoginFacebook(request):
    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 2:
                login(request, account)
                
                return redirect("admin:index")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}
    
    return render(request, "officer/login/facebook.html", context)


def OfficerLoginGoogle(request):
    if request.method == "POST":
        username = request.POST.get("username")
        
        password = request.POST.get("password1")
        
        account = authenticate(request, username = username, password = password)

        if account:
            if account.usertype_id == 2:
                login(request, account)
                
                return redirect("admin:index")
            
            else:
                messages.error(request, "Username or password is not valid.")
        
        else:
            messages.error(request, "Username or password is not valid.")

    context = {}
    
    return render(request, "officer/login/google.html", context)


@login_required(login_url = "Officer Login")
def OfficerLogout(request):
    username = request.user.username

    logout(request)
    
    messages.success(request, username + ", " + "your account used just now was signed out of COTSEye.")
    
    return redirect("Officer Login")


def AdministratorLogin(request):
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

    return render(request, "admin/login/login.html", context)


@login_required(login_url = "Administrator Login")
def AdministratorLogout(request):
    user = request.user
    
    username = request.user.username

    if user.usertype_id == 1:
        logout(request)
        
        messages.success(request, username + ", " + "your account used just now was signed out of COTSEye.")
        
        return redirect("Administrator Login")
    
    elif user.usertype_id == 2:
        logout(request)
        
        messages.success(request, username + ", " + "your account used just now was signed out of COTSEye.")
        
        return redirect("Officer Logout")