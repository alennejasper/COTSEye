from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Intervention, Status, StatusType
from datetime import date

# @receiver(post_save, sender=Intervention)
# def create_status(sender, instance, created, **kwargs):
#     if created:
#         location = instance.location
#         caught_amount = instance.caught_amount

#         # Get the most recent Status entry for the same location by primary key (last entry created)
#         latest_status = Status.objects.filter(location=location).order_by('-id').first()

     
#         new_caught_overall = caught_amount

#         # Determine the status type based on the new caught_overall
#         if new_caught_overall < 100:
#             statustype = StatusType.objects.get(is_low=True)
#         elif 100 <= new_caught_overall <= 500:
#             statustype = StatusType.objects.get(is_moderate=True)
#         else:
#             statustype = StatusType.objects.get(is_critical=True)

#         # Create a new Status entry
#         Status.objects.create(
#             location=location,
#             statustype=statustype,
#             caught_overall=new_caught_overall,
#             onset_date=date.today()
#         )
