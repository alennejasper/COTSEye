from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import mark_safe

import datetime


# Create your models here.
class Location(models.Model):
    barangay = models.CharField(max_length = 65, help_text = "Designates the name of the barangay.", verbose_name = "Barangay")
    municipality = models.CharField(max_length = 65, help_text = "Designates the name of the municipality.", verbose_name = "Municipality")
    latitude = models.DecimalField(null = True, blank = True, max_digits = 27, decimal_places = 7, help_text = "Designates the latitude of the location.", verbose_name = "Default Pin Latitude")
    longitude = models.DecimalField(null = True, blank = True, max_digits = 27, decimal_places = 7, help_text = "Designates the longitude of the location.", verbose_name = "Default Pin Longitude")
    perimeters = models.TextField(null = True, blank = True, max_length = 15000, help_text = "Designates the perimeters of the location.", verbose_name = "Map Perimeters")
    
    class Meta:
        db_table = "managements_location"
        verbose_name = "Location"
        verbose_name_plural = "Location"
    
    def __str__(self):
        return str(self.barangay) + ", " + str(self.municipality)


class StatusType(models.Model):
    statustype = models.CharField(default = "None", null = True, max_length = 65, help_text = "Designates the status type.", verbose_name = "Status Level Type")
    
    class Meta:
        db_table = "managements_status_type"
        verbose_name = "Status Level Type"
        verbose_name_plural = "Status Level Type"

    def __str__(self):
        return str(self.statustype)

class Status(models.Model):
    location = models.ForeignKey(Location, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Location model.", verbose_name = "Location")
    statustype = models.ForeignKey(StatusType, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Status Type model.", verbose_name = "Status Type")
    caught_overall = models.IntegerField(validators = [MinValueValidator(0)], help_text = "Designates the overall amount of the caught Crown-of-Thorns Starfish at the moment.", verbose_name = "Caught Overall")
    volunteer_overall = models.IntegerField(null=True, blank=True, validators = [MinValueValidator(0)], help_text = "Designates the overall amount of the volunteers at the moment the intervention took place.", verbose_name = "Volunteer Overall")
    onset_date = models.DateField(default = datetime.date.today(), help_text = "Designates the onset date of the outbreak status.", verbose_name = "Onset Date")

    class Meta:
        db_table = "managements_status"
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
    
    def __str__(self):
        return "STATUS " + str(self.id) + " | " +  str(self.location)


class Intervention(models.Model):
    title = models.CharField(max_length = 150, help_text = "Designates the title of the activity.", verbose_name = "Title")
    location = models.ForeignKey(Location, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Location model.", verbose_name = "Location")
    statustype = models.ForeignKey(StatusType, null = True, blank = True, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Status Type model.", verbose_name = "Status Type")
    volunteer_amount = models.IntegerField(null = True, blank = True, validators = [MinValueValidator(0)], help_text = "Designates the amount of the volunteers at the moment the activity took place.", verbose_name = "Volunteer Amount")
    caught_amount = models.IntegerField(null = True, blank = True, validators = [MinValueValidator(0)], help_text = "Designates the amount of the caught Crown-of-Thorns Starfish at the moment the activity took place.", verbose_name = "Caught Amount")
    details = models.TextField(max_length=5000, help_text = "Designates the details of the activity.", verbose_name = "Details")
    hosting_agency = models.CharField(max_length = 150, help_text = "Designates the name of the hosting agency.", verbose_name = "Hosting Agency")
    intervention_photo = models.ImageField(default = "interventions/default.png", upload_to = "interventions", help_text = "Designates the photo of the activity.", verbose_name = "Intervention Photo")
    intervention_date = models.DateField(default = datetime.date.today(), help_text = "Designates the date of the activity.", verbose_name = "Activity Date")
    creation_date = models.DateTimeField(default = datetime.datetime.now, help_text = "Designates the creation date and time of the activity.", verbose_name = "Creation Date")
    class Meta:
        db_table = "managements_intervention"
        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"

    def gallery_photo(self):
        if self.intervention_photo != "":
            return mark_safe("<img src='%s%s'/>" % (f"{settings.MEDIA_URL}", self.intervention_photo))

    gallery_photo.short_description = "Gallery Photo"

    def __str__(self):
        return str(self.title) + " | " + str(self.intervention_date.strftime("%b. %d, %Y"))

    def save(self, *args, **kwargs):
        if self.caught_amount is not None:
            if 0 <= self.caught_amount <= 5:
                self.statustype = StatusType.objects.get(statustype = "None")

            if 6 <= self.caught_amount <= 12:
                self.statustype = StatusType.objects.get(statustype = "Low")

            elif 13 <= self.caught_amount <= 18:
                self.statustype = StatusType.objects.get(statustype = "Medium")
            
            elif 19 <= self.caught_amount <= 24:
                self.statustype = StatusType.objects.get(statustype = "High")
            
            elif self.caught_amount >= 25:
                self.statustype = StatusType.objects.get(statustype = "Critical")

        super(Intervention, self).save(*args, **kwargs)

        start_of_year = datetime.date(self.intervention_date.year, 1, 1)

        end_of_year = datetime.date(self.intervention_date.year, 12, 31)

        interventions_in_year = Intervention.objects.filter(location = self.location, intervention_date__range = (start_of_year, end_of_year))

        caught_overall = interventions_in_year.aggregate(models.Sum("caught_amount"))["caught_amount__sum"] or 0
        
        volunteer_overall = interventions_in_year.aggregate(models.Sum("volunteer_amount"))["volunteer_amount__sum"] or 0

        Status.objects.create(location = self.location, statustype = self.statustype, caught_overall = caught_overall, volunteer_overall = volunteer_overall, onset_date = self.intervention_date)