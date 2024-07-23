from .models import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from authentications.models import Account


# Create your signals here.
@receiver(post_save, sender = PostPhoto)
def AddPostPhotoLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = PostPhoto)
def UpdatePostPhotoLog(sender, instance, **kwargs):
    if instance.id:
        try:
            post_photo = PostPhoto.objects.get(id = instance.id)

        except PostPhoto.DoesNotExist:
            post_photo = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if post_photo:
            if instance.post_photo != post_photo.post_photo:
                changes.append("Changed Post Photo")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = PostPhoto)
def DeletePostPhotoLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Coordinates)
def AddCoordinatesLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Coordinates)
def UpdateCoordinatesLog(sender, instance, **kwargs):
    if instance.id:
        try:
            coordinates = Coordinates.objects.get(id = instance.id)

        except Coordinates.DoesNotExist:
            coordinates = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if coordinates:
            if instance.latitude != coordinates.latitude:
                changes.append("Changed Latitude")
            
            if instance.longitude != coordinates.longitude:
                changes.append("Changed Longitude")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Coordinates)
def DeleteCoordinatesLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = PostStatus)
def AddPostStatusLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = PostStatus)
def UpdatePostStatusLog(sender, instance, **kwargs):
    if instance.id:
        try:
            post_status = PostStatus.objects.get(id = instance.id)

        except PostStatus.DoesNotExist:
            post_status = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if post_status:
            if instance.is_valid != post_status.is_valid:
                changes.append("Changed Valid")
            
            if instance.is_invalid != post_status.is_invalid:
                changes.append("Changed Invalid")

            if instance.is_pending != post_status.is_pending:
                changes.append("Changed Pending")

            if instance.is_invalid != post_status.is_draft:
                changes.append("Changed Draft")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = PostStatus)
def DeletePostStatusLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Size)
def AddSizeLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Size)
def UpdateSizeLog(sender, instance, **kwargs):
    if instance.id:
        try:
            size = Size.objects.get(id = instance.id)

        except Size.DoesNotExist:
            size = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if size:
            if instance.size != size.size:
                changes.append("Changed Size")
            
            if instance.description != size.description:
                changes.append("Changed Description")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Size)
def DeleteSizeLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = Depth)
def AddDepthLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Depth)
def UpdateDepthLog(sender, instance, **kwargs):
    if instance.id:
        try:
            depth = Depth.objects.get(id = instance.id)

        except Depth.DoesNotExist:
            depth = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if depth:
            if instance.depth != depth.depth:
                changes.append("Changed Depth")
            
            if instance.description != depth.description:
                changes.append("Changed Description")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = Depth)
def DeleteDepthLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_save, sender = PostObservation)
def AddPostObservationLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = PostObservation)
def UpdatePostObservationLog(sender, instance, **kwargs):
    if instance.id:
        try:
            post_observation = PostObservation.objects.get(id = instance.id)

        except PostObservation.DoesNotExist:
            post_observation = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if post_observation:
            if instance.size != post_observation.size:
                changes.append("Changed Size")
            
            if instance.depth != post_observation.depth:
                changes.append("Changed Depth")
            
            if instance.density != post_observation.density:
                changes.append("Changed Density")
            
            if instance.weather != post_observation.weather:
                changes.append("Changed Weather")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(post_delete, sender = PostObservation)
def DeletePostObservationLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())      


@receiver(post_save, sender = Post)
def AddPostLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = Post)
def UpdatePostLog(sender, instance, **kwargs):
    if instance.id:
        try:
            post = Post.objects.get(id = instance.id)

        except Post.DoesNotExist:
            post = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if post:
            if instance.user != post.user:
                changes.append("Changed User")
            
            if instance.validator != post.validator:
                changes.append("Changed Validator")

            if instance.description != post.description:
                changes.append("Changed Description")
            
            if instance.coordinates.id != post.coordinates.id:
                changes.append("Changed Coordinates")
            
            if instance.location.id != post.location.id:
                changes.append("Changed Location")

            if instance.post_status.id != post.post_status.id:
                changes.append("Changed Post Status")
            
            if instance.post_observation.id != post.post_observation.id:
                changes.append("Changed Post Observation")

            if instance.remarks != post.remarks:
                changes.append("Added Remarks")

            if instance.post_photos != post.post_photos:
                changes.append("Changed Post Photos")

            if instance.capture_date != post.capture_date:
                changes.append("Changed Capture Date")
            
            if instance.creation_date != post.creation_date:
                changes.append("Changed Creation Date")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())      


@receiver(post_delete, sender = Post)
def DeletePostLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())
        

@receiver(post_save, sender = PostGallery)
def AddPostGalleryLog(sender, instance, created, **kwargs):
    if created:
        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())


@receiver(pre_save, sender = PostGallery)
def UpdatePostGalleryLog(sender, instance, **kwargs):
    if instance.id:
        try:
            post_gallery = PostGallery.objects.get(id = instance.id)

        except PostGallery.DoesNotExist:
            post_gallery = None

        import inspect

        for information in inspect.stack():
            if information[3] == "get_response":
                request = information[0].f_locals["request"]

                break

            else:
                request = None

        changes = []
        
        if post_gallery:
            if instance.post_photos != post_gallery.post_photos:
                changes.append("Changed Post Photos")
            
            if instance.post != post_gallery.post:
                changes.append("Changed Post")
                
            if changes:
                message = ", ".join(changes)

                LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = request.user.username), action_time = timezone.now())

                
@receiver(post_delete, sender = PostGallery)
def DeletePostGalleryLog(sender, instance, **kwargs):
    import inspect

    for information in inspect.stack():
        if information[3] == "get_response":
            request = information[0].f_locals["request"]

            break

        else:
            request = None

    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted.", user = Account.objects.get(username = request.user.username), action_time = timezone.now())