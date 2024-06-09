from .models import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from authentications.models import Account


@receiver(pre_save, sender = Post)
def UpdateLog(sender, instance, **kwargs):
    if instance.id:
        try:
            post = Post.objects.get(id = instance.id)

        except Post.DoesNotExist:
            post = None

        changes = []
        
        if post:
            if instance.description != post.description:
                changes.append("Changed Description")
            
            if instance.capture_date != post.capture_date:
                changes.append("Changed Capture Date")
            
            if instance.post_photos != post.post_photos:
                changes.append("Changed Post Photos")
            
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
                
            if changes:
                message = ", ".join(changes)

                if instance.validated_by is None:
                    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = instance.user.account.username), action_time = timezone.now())
                
                else:
                    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = CHANGE, change_message = message, user = Account.objects.get(username = instance.validated_by.account.username), action_time = timezone.now())


@receiver(post_save, sender = Post)
def AddLog(sender, instance, created, **kwargs):
    if created:
        LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = ADDITION, change_message = "Added Object", user = Account.objects.get(username = instance.user.account.username), action_time = timezone.now())


@receiver(post_delete, sender = Post)
def DeleteLog(sender, instance, **kwargs):
    LogEntry.objects.create(content_type = ContentType.objects.get_for_model(instance), object_id = instance.id, object_repr = str(instance), action_flag = DELETION, change_message = "Deleted Object", user = Account.objects.get(username = instance.user.account.username), action_time = timezone.now())
