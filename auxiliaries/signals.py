from .models import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from authentications.models import Account


# Create your signals here.
@receiver(post_save, sender = File)
def AddFileLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = File)
def UpdateFileLog(sender, instance, **kwargs):
    if instance.id:
        try:
            file = File.objects.get(id = instance.id)

        except File.DoesNotExist:
            file = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if file:
            if instance.author != file.author:
                changes.append("Changed Author")
            
            if instance.title != file.title:
                changes.append("Changed Title")
            
            if instance.resource_file != file.resource_file:
                changes.append("Changed Resource File")
            
            if instance.release_date != file.release_date:
                changes.append("Changed Release Date")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = File)
def DeleteFileLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Inquiry)
def AddInquiryLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Inquiry)
def UpdateInquiryLog(sender, instance, **kwargs):
    if instance.id:
        try:
            inquiry = Inquiry.objects.get(id = instance.id)

        except Inquiry.DoesNotExist:
            inquiry = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if inquiry:
            if instance.question != inquiry.question:
                changes.append("Changed Question")
            
            if instance.answer != inquiry.answer:
                changes.append("Changed Answer")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Inquiry)
def DeleteInquiryLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Link)
def AddLinkLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Link)
def UpdateLinkLog(sender, instance, **kwargs):
    if instance.id:
        try:
            link = Link.objects.get(id = instance.id)

        except Link.DoesNotExist:
            link = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if link:
            if instance.author != link.author:
                changes.append("Changed Author")
            
            if instance.title != link.title:
                changes.append("Changed Title")
            
            if instance.resource_link != link.resource_link:
                changes.append("Changed Resource Link")
            
            if instance.release_date != link.release_date:
                changes.append("Changed Release Date")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Link)
def DeleteLinkLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())