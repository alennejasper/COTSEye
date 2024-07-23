from .models import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from managements.models import Intervention, Announcement
from reports.models import Post, PostStatus
from django.db.models import Q


# Create your signals here.
@receiver(post_save, sender = UserType)
def AddUserTypeLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        if request:
            LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = UserType)
def UpdateUserTypeLog(sender, instance, **kwargs):
    if instance.id:
        try:
            usertype = UserType.objects.get(id = instance.id)

        except UserType.DoesNotExist:
            usertype = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if usertype:
            if instance.is_superuser != usertype.is_superuser:
                changes.append("Changed Administrator")
            
            if instance.is_staff != usertype.is_staff:
                changes.append("Changed Officer")
            
            if instance.is_contributor != usertype.is_contributor:
                changes.append("Changed Contributor")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = UserType)
def DeleteUserTypeLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Account)
def AddAccountLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

            if request:
                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Account)
def UpdateAccountLog(sender, instance, **kwargs):
    if instance.id:
        try:
            account = Account.objects.get(id = instance.id)

        except Account.DoesNotExist:
            account = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if account:
            if instance.username != account.username:
                changes.append("Changed Username")
            
            if instance.password != account.password:
                changes.append("Changed Password")
            
            if instance.usertype != account.usertype:
                changes.append("Changed Usertype")
            
            if instance.is_active != account.is_active:
                administrator = request.user.username

                officers = User.objects.filter(account = account)

                for officer in officers:
                    subject = "COTSEye has delivered an alert message!"

                    scheme = request.scheme

                    host = request.META["HTTP_HOST"]

                    template = render_to_string("admin/control/profile/email.html", {"officer": officer.account.username, "administrator": administrator, "scheme": scheme, "host": host})

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
                                
                changes.append("Changed Active Status")

            if instance.last_login != account.last_login:
                changes.append("Changed Last Login")
            
            if instance.groups != account.groups:
                changes.append("Changed Groups")
            
            if instance.user_permissions != account.user_permissions:
                changes.append("Changed User Permissions")
                
            if changes:
                message = ", ".join(changes)

                if Account.DoesNotExist():
                    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = account.username), action_time = timezone.now())

                else:
                    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Account)
def DeleteAccountLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = User)
def AddUserLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

            if request:
                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = User)
def UpdateUserLog(sender, instance, **kwargs):
    if instance.id:
        try:
            user = User.objects.get(id = instance.id)

        except User.DoesNotExist:
            user = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if user:
            if instance.account != user.account:
                changes.append("Changed Account")
            
            if instance.first_name != user.first_name:
                changes.append("Changed First Name")
            
            if instance.last_name != user.last_name:
                changes.append("Changed Last Name")
            
            if instance.email != user.email:
                changes.append("Changed Email")
            
            if instance.phone_number != user.phone_number:
                changes.append("Changed Phone Number")
            
            if instance.profile_photo != user.profile_photo:
                changes.append("Changed Profile Photo")
            
            if instance.joined_date != user.joined_date:
                changes.append("Changed Joined Date")
                
            if changes:
                message = ", ".join(changes)
                
                if Account.DoesNotExist():
                    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = user.account.username), action_time = timezone.now())

                else:
                    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = User)
def DeleteUserLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


def AddNotification(notification_type, instance, sender, user_filter):
    users = User.objects.filter(user_filter)

    content_type = ContentType.objects.get_for_model(sender)

    for user in users:
        Notification.objects.create(notificationtype = notification_type, user = user, object = instance, contenttype = content_type, key = instance.id)
        

@receiver(post_save, sender = Post)
@receiver(post_save, sender = Announcement)
@receiver(post_save, sender = Intervention)
def SendNotification(sender, instance, created, **kwargs):
    if created:
        if sender == Post:
            notification_type = "post"

            user_filter = Q(account__usertype__is_staff = True)

        elif sender == Announcement:
            notification_type = "announcement"

            user_filter =  Q(account__usertype__is_contributor = True)

        elif sender == Intervention:
            notification_type = "intervention"

            user_filter =  Q(account__usertype__is_contributor = True)
        
        AddNotification(notification_type, instance, sender, user_filter)


@receiver(post_save, sender = Post)
def UpdateNotification(sender, instance, created, **kwargs):
    if not created and instance.validator:
        if instance.validator.account.usertype.is_staff:
            notification_type = "post_valid"

            user_filter = Q(id = instance.user.id)

            AddNotification(notification_type, instance, sender, user_filter)


@receiver(post_save, sender = Post)
def AddBadge(sender, instance, created, **kwargs):
    if instance.post_status.is_valid:
        user = instance.user

        post_count = Post.objects.filter(user = user, post_status__is_valid = True).count()

        award = []

        if post_count == 1:
            award.append(Badge.objects.get(badge_name = "First Sighting"))

        elif post_count == 25:
            award.append(Badge.objects.get(badge_name = "25 Sightings"))

        elif post_count == 50:
            award.append(Badge.objects.get(badge_name = "50 Sightings"))


        top_reporter = Post.objects.filter(post_status__is_valid = True).values("user").annotate(count = models.Count("id")).order_by("-count").first()
        
        if top_reporter and top_reporter["user"] == user.id:
            award.append(Badge.objects.get(badge_name = "Top Reporter"))

        for badge in award:
            user.badges.add(badge)

            Notification.objects.create(user = user, notificationtype = "achievement", object = badge, contenttype = ContentType.objects.get_for_model(badge), key = badge.id)