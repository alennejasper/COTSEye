from django.db import models

import datetime


# Create your models here.
class Location(models.Model):
    barangay = models.CharField(max_length = 65, null = True, blank = True, help_text = "Designates the name of the barangay.", verbose_name = "Barangay")
    municipality = models.CharField(max_length = 65, null = True, blank = True, help_text = "Designates the name of the municipality.", verbose_name = "Municipality")
    perimeters = models.TextField(max_length = 15000, null = True, blank = True, help_text = "Designates the perimeters of the location.", verbose_name = "Perimeters")
    
    class Meta:
        db_table = "managements_location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"
    
    def __str__(self):
        return "Barangay " + str(self.barangay) + ", " + str(self.municipality)


class StatusType(models.Model):
    is_critical = models.BooleanField(default = False, help_text = "Designates that the status is critical.", verbose_name = "Critical Status")
    is_moderate = models.BooleanField(default = False, help_text = "Designates that the status is moderate.", verbose_name = "Moderate Status")
    is_low = models.BooleanField(default = False, help_text = "Designates that the status is low.", verbose_name = "Low Status")
    
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
    location = models.ForeignKey(Location, on_delete = models.CASCADE, null = True, blank = True, help_text = "Designates the foreign key of the Location model.", verbose_name = "Location")
    statustype = models.ForeignKey(StatusType, on_delete = models.SET_NULL, blank = True, null = True, help_text = "Designates the foreign key of the Status Type model.", verbose_name = "Status Type")
    onset_date = models.DateField(default = datetime.date.today(), help_text = "Designates the onset date of the outbreak status.", verbose_name = "Status Date")

    class Meta:
        db_table = "managements_status"
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
    
    def __str__(self):
        return "STATUS " + str(self.id) + " | " + self.onset_date.strftime("%B %d, %Y")