from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from authentications.models import User

import datetime


# Create your models here.
class Municipality(models.Model):
    municipality_name = models.CharField(unique = True, error_messages = {"unique": "This municipality already exist."}, max_length = 65, verbose_name = "Municipality Name")
    
    class Meta:
        db_table = "managements_municipality"
        verbose_name = "Municipality"
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return self.municipality_name


class Barangay(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete = models.CASCADE, verbose_name = "Municipality Name")
    barangay_name = models.CharField(unique = True, error_messages = {"unique": "This barangay already exist."}, max_length = 65, verbose_name = "Barangay Name")

    class Meta:
        db_table = "managements_barangay"
        verbose_name = "Barangay"
        verbose_name_plural = "Barangays"
    
    def __str__(self):
        return self.barangay_name


class Location(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete = models.CASCADE, verbose_name = "Municipality")
    barangay = models.ForeignKey(Barangay, on_delete = models.CASCADE, related_name = "locations", verbose_name = "Barangay")
    latitude = models.DecimalField(max_digits = 27, decimal_places = 7, verbose_name = "Default Pin Latitude")
    longitude = models.DecimalField(max_digits = 27, decimal_places = 7, verbose_name = "Default Pin Longitude")
    perimeters = models.TextField(verbose_name = "Barangay Perimeter")

    class Meta:
        db_table = "managements_location"
        verbose_name = "Location"
        verbose_name_plural = "Location"
    
    def __str__(self):
        return str(self.barangay.barangay_name) + ", " + str(self.municipality.municipality_name)
    
    def clean(self):
        if self.barangay.municipality != self.municipality:
            raise ValidationError("The selected barangay does not belong to the selected municipality.")
        
    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)


class StatusType(models.Model):
    statustype = models.CharField(unique = True, error_messages = {"unique": "This infestation level already exist."}, null = True, max_length = 65, verbose_name = "Infestation Level")
    description = models.TextField(max_length = 255, verbose_name = "Description")
    class Meta:
        db_table = "managements_status_type"
        verbose_name = "Infestation Level"
        verbose_name_plural = "Infestation Level"

    def __str__(self):
        return str(self.statustype) + " (" + str(self.description) + ") " 


class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "User")
    hosting_agency = models.CharField(null = True, blank = True, max_length = 150, verbose_name = "Hosting Agency")
    title = models.CharField(max_length = 150, verbose_name = "Title")
    context = models.TextField(null = True, blank = True, max_length = 5000, verbose_name = "Context")
    location = models.ForeignKey(Location, null = True, blank = True, on_delete = models.CASCADE, verbose_name = "Location")
    announcement_photo = models.ImageField(default = "announcements/default.png", null = True, upload_to = "announcements", verbose_name = "Announcement Photo")
    event_date = models.DateTimeField(default = datetime.datetime.now, verbose_name = "Event Date")
    creation_date = models.DateTimeField(default = datetime.datetime.now, verbose_name = "Creation Date")

    class Meta:
        db_table = "managements_announcement"
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def gallery_photo(self):
        if self.announcement_photo != "":
            return mark_safe("<img src = '%s%s'/>" % (f"{settings.MEDIA_URL}", self.announcement_photo))
    
    gallery_photo.short_description = "Gallery Photo"
    
    def get_photo_url(self):
        if self.announcement_photo and hasattr(self.announcement_photo, "url"):
            return self.announcement_photo.url
        
        else:
            return settings.MEDIA_URL + "announcements/default.png"
        
    def __str__(self):
        return str(self.title) + " (" + str(self.event_date) + ") " 
    

class Activity(models.Model):
    hosting_agency = models.CharField(max_length = 150, verbose_name = "Hosting Agency")
    title = models.CharField(max_length = 150, verbose_name = "Title")
    details = models.TextField(max_length = 5000, verbose_name = "Details")
    location = models.ForeignKey(Location, on_delete = models.CASCADE, verbose_name = "Location")
    statustype = models.ForeignKey(StatusType, null = True, blank = True, on_delete = models.CASCADE, verbose_name = "Status Type")
    volunteer_amount = models.IntegerField(null = True, blank = True, validators = [MinValueValidator(0)], verbose_name = "Volunteer Amount")
    caught_amount = models.IntegerField(null = True, blank = True, validators = [MinValueValidator(0)], verbose_name = "Caught Amount")
    activity_photo = models.ImageField(default = "activities/default.png", upload_to = "activities", verbose_name = "Activity Photo")
    activity_date = models.DateField(default = datetime.date.today, verbose_name = "Activity Date")
    creation_date = models.DateTimeField(default = datetime.datetime.now, verbose_name = "Creation Date")

    class Meta:
        db_table = "managements_activity"
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def gallery_photo(self):
        if self.activity_photo != "":
            return mark_safe("<img src = '%s%s'/>" % (f"{settings.MEDIA_URL}", self.activity_photo))

    gallery_photo.short_description = "Gallery Photo"

    def __str__(self):
        return str(self.title) + " (" + str(self.activity_date.strftime("%b. %d, %Y")) + ") "
    
    def save(self, *args, **kwargs):
        if self.caught_amount is not None:
            if 1 <= self.caught_amount <= 5:
                self.statustype = StatusType.objects.get(statustype = "Vey Low")

            elif 6 <= self.caught_amount <= 12:
                self.statustype = StatusType.objects.get(statustype = "Low")

            elif 13 <= self.caught_amount <= 18:
                self.statustype = StatusType.objects.get(statustype = "Moderate")

            elif 19 <= self.caught_amount <= 24:
                self.statustype = StatusType.objects.get(statustype = "High")

            elif self.caught_amount >= 25:
                self.statustype = StatusType.objects.get(statustype = "Critical")

        super(Activity, self).save(*args, **kwargs)

        status, created = Status.objects.update_or_create(activity = self, defaults = {"location": self.location, "statustype": self.statustype, "caught_overall": self.caught_amount or 0, "volunteer_overall": self.volunteer_amount or 0, "onset_date": self.activity_date})
    

class Status(models.Model):
    location = models.ForeignKey(Location, on_delete = models.CASCADE, verbose_name = "Location")
    activity = models.ForeignKey("Activity", on_delete = models.CASCADE, null = True, blank = True, verbose_name = "Activity")    
    statustype = models.ForeignKey(StatusType, on_delete = models.CASCADE, verbose_name = "Status Type")
    caught_overall = models.IntegerField(validators = [MinValueValidator(0)], verbose_name = "Caught Overall")
    volunteer_overall = models.IntegerField(null = True, blank = True, validators = [MinValueValidator(0)], verbose_name = "Volunteer Overall")
    onset_date = models.DateField(default = datetime.datetime.now, verbose_name = "Onset Date")
    creation_date = models.DateTimeField(default = datetime.datetime.now, verbose_name = "Creation Date")

    class Meta:
        db_table = "managements_status"
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
    
    def __str__(self):
        return "STATUS " + str(self.id) + " (" + str(self.location) + ") "