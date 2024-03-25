from django.db import models
from django.core.validators import MinValueValidator

import datetime


# Create your models here.
class Location(models.Model):
    barangay = models.CharField(max_length = 65, help_text = "Designates the name of the barangay.", verbose_name = "Barangay")
    municipality = models.CharField(max_length = 65, help_text = "Designates the name of the municipality.", verbose_name = "Municipality")
    perimeters = models.TextField(max_length = 15000, help_text = "Designates the perimeters of the location.", verbose_name = "Perimeters")
    
    class Meta:
        db_table = "managements_location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"
    
    def __str__(self):
        return "Barangay " + str(self.barangay) + ", " + str(self.municipality)


class StatusType(models.Model):
    is_critical = models.BooleanField(default = False, help_text = "Designates that the status is critical.", verbose_name = "Critical")
    is_moderate = models.BooleanField(default = False, help_text = "Designates that the status is moderate.", verbose_name = "Moderate")
    is_low = models.BooleanField(default = False, help_text = "Designates that the status is low.", verbose_name = "Low")
    
    class Meta:
        db_table = "managements_status_type"
        verbose_name = "Status Type"
        verbose_name_plural = "Status Types"

    def __str__(self):
        if self.is_critical == True:
            return "Critical"
        
        elif self.is_moderate == True:
            return "Moderate"
        
        elif self.is_low == True:
            return "Low"

class Status(models.Model):
    location = models.ForeignKey(Location, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Location model.", verbose_name = "Location")
    statustype = models.ForeignKey(StatusType, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Status Type model.", verbose_name = "Status Type")
    caught_overall = models.IntegerField(validators = [MinValueValidator(0)], help_text = "Designates the overall amount of the caught Crown-of-Thorns Starfish at the moment.", verbose_name = "Caught Amount")
    onset_date = models.DateField(default = datetime.date.today(), help_text = "Designates the onset date of the outbreak status.", verbose_name = "Onset Date")

    class Meta:
        db_table = "managements_status"
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
    
    def __str__(self):
        return "STATUS " + str(self.id) + " | " +  str(self.location)


class Intervention(models.Model):
    title = models.CharField(max_length = 150, help_text = "Designates the title of the intervention.", verbose_name = "Title")
    location = models.ForeignKey(Location, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Location model.", verbose_name = "Location")
    caught_amount = models.IntegerField(validators = [MinValueValidator(0)], help_text = "Designates the amount of the caught Crown-of-Thorns Starfish at the moment the intervention took place.", verbose_name = "Caught Amount")
    details = models.TextField(max_length = 5000, help_text = "Designates the details of the intervention.", verbose_name = "Details")
    hosting_agency = models.CharField(max_length = 150, help_text = "Designates the name of the hosting agency.", verbose_name = "Hosting Agency")
    intervention_photo = models.ImageField(default = "interventions/default.png", upload_to = "interventions", help_text = "Designates the photo of the intervention.", verbose_name = "Intervention Photo")
    intervention_date = models.DateField(default = datetime.date.today(), help_text = "Designates the date of the intervention.", verbose_name = "Intervention Date")

    class Meta:
        db_table = "managements_intervention"
        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"
    
    def __str__(self):
        return str(self.title) + " | " +  str(self.intervention_date.strftime("%b. %d, %Y"))