from .models import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from authentications.models import Account
from reports.models import Post
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


# Create your signals here.
@receiver(post_save, sender = Municipality)
def AddMunicipalityLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Municipality)
def UpdateMunicipalityLog(sender, instance, **kwargs):
    if instance.id:
        try:
            municipality = Municipality.objects.get(id = instance.id)

        except Municipality.DoesNotExist:
            municipality = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if municipality:
            if instance.municipality_name != municipality.municipality_name:
                changes.append("Changed Municipality Name")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Municipality)
def DeleteMunicipalityLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Barangay)
def AddBarangayLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Barangay)
def UpdateBarangayLog(sender, instance, **kwargs):
    if instance.id:
        try:
            barangay = Barangay.objects.get(id = instance.id)

        except Barangay.DoesNotExist:
            barangay = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if barangay:
            if instance.municipality != barangay.municipality:
                changes.append("Changed Municipality")
                
            if instance.barangay_name != barangay.barangay_name:
                changes.append("Changed Barangay Name")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Barangay)
def DeleteBarangayLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Location)
def AddLocationLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Location)
def UpdateLocationLog(sender, instance, **kwargs):
    if instance.id:
        try:
            location = Location.objects.get(id = instance.id)

        except Location.DoesNotExist:
            location = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if location:
            if instance.municipality != location.municipality:
                changes.append("Changed Municipality")
            
            if instance.barangay != location.barangay:
                changes.append("Changed Barangay")

            if instance.latitude != location.latitude:
                changes.append("Changed Latitude")

            if instance.longitude != location.longitude:
                changes.append("Changed Longitude")

            if instance.perimeters != location.perimeters:
                changes.append("Changed Perimeters")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Location)
def DeleteLocationLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = StatusType)
def AddStatusTypeLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = StatusType)
def UpdateStatusTypeLog(sender, instance, **kwargs):
    if instance.id:
        try:
            statustype = StatusType.objects.get(id = instance.id)

        except StatusType.DoesNotExist:
            statustype = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if statustype:
            if instance.statustype != statustype.statustype:
                changes.append("Changed Status Type")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = StatusType)
def DeleteStatusTypeLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Status)
def AddStatusLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Status)
def UpdateStatusLog(sender, instance, **kwargs):
    if instance.id:
        try:
            status = Status.objects.get(id = instance.id)

        except Status.DoesNotExist:
            status = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if status:
            if instance.location != status.location:
                changes.append("Changed Location")
            
            if instance.intervention != status.intervention:
                changes.append("Changed Intervention")
            
            if instance.statustype != status.statustype:
                changes.append("Changed Status Type")
            
            if instance.caught_overall != status.caught_overall:
                changes.append("Changed Caught Overall")

            if instance.volunteer_overall != status.volunteer_overall:
                changes.append("Changed Volunteer Overall")

            if instance.onset_date != status.onset_date:
                changes.append("Changed Onset Date")
            
            if instance.creation_date != status.creation_date:
                changes.append("Changed Creation Date")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Status)
def DeleteStatusLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Announcement)
def AddAnnouncementLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Announcement)
def UpdateAnnouncementLog(sender, instance, **kwargs):
    if instance.id:
        try:
            announcement = Announcement.objects.get(id = instance.id)

        except Announcement.DoesNotExist:
            announcement = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if announcement:
            if instance.user != announcement.user:
                changes.append("Changed User")
            
            if instance.hosting_agency != announcement.hosting_agency:
                changes.append("Changed Hosting Agency")
            
            if instance.title != announcement.title:
                changes.append("Changed Title")
            
            if instance.context != announcement.context:
                changes.append("Changed Context")
            
            if instance.location != announcement.location:
                changes.append("Changed Location")
            
            if instance.announcement_photo != announcement.announcement_photo:
                changes.append("Changed Announcement Photo")
            
            if instance.release_date != announcement.release_date:
                changes.append("Changed Release Date")
            
            if instance.creation_date != announcement.creation_date:
                changes.append("Changed Creation Date")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Announcement)
def DeleteAnnouncementLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Intervention)
def AddInterventionLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Intervention)
def UpdateInterventionLog(sender, instance, **kwargs):
    if instance.id:
        try:
            intervention = Intervention.objects.get(id = instance.id)

        except Intervention.DoesNotExist:
            intervention = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if intervention:
            if instance.title != intervention.title:
                changes.append("Changed Title")
            
            if instance.details != intervention.details:
                changes.append("Changed Details")

            if instance.location != intervention.location:
                changes.append("Changed Location")
            
            if instance.statustype != intervention.statustype:
                changes.append("Changed Status Type")
            
            if instance.volunteer_amount != intervention.volunteer_amount:
                changes.append("Changed Volunteer Amount")
            
            if instance.caught_amount != intervention.caught_amount:
                changes.append("Changed Caught Amount")
            
            if instance.intervention_photo != intervention.intervention_photo:
                changes.append("Changed Intervention Photo")
            
            if instance.event_date != intervention.event_date:
                changes.append("Changed Event Date")
            
            if instance.creation_date != intervention.creation_date:
                changes.append("Changed Creation Date")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Intervention)
def DeleteInterventionLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())