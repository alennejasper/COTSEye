from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone
from .models import *

import datetime


def validate_not_past_date(value):
    if value < timezone.now():
        raise ValidationError("The release date cannot be in the past.")
    
class AnnouncementForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Announcement
        fields = ["title", "release_date", "context", "hosting_agency", "announcement_photo"]
        widgets = {"title": forms.TextInput(attrs = {"class": "form-control", "id": "announcementTitle", "required": True}), "release_date": forms.DateInput(attrs = {"class": "form-control", "id": "announcementDate", "type": "date", "required": True}), "context": forms.Textarea(attrs = {"class": "form-control", "id": "announcementDescription", "rows": 3, "required": False}), "announcement_photo": forms.FileInput(attrs = {"class": "form-control", "id": "announcementPhoto"}),"hosting_agency": forms.TextInput(attrs = {"class": "form-control", "id": "hostingAgency", "required": True})}
        help_texts = {"title": None, "release_date": None, "context": None, "announcement_photo": None}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

    def clean_release_date(self):
        release_date = self.cleaned_data.get("release_date")
        
        if release_date < timezone.now():
            raise ValidationError("The date cannot be in the past.")
        
        return release_date

    def save(self, commit = True):
        instance = super().save(commit = False)
 
        if self.user:
            instance.user = self.user

        if commit:
            instance.save()

        return instance
    

def validate_not_future_date(value):
    if value > date.today():
        raise ValidationError("The date cannot be in the future.")
    

class InterventionForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Intervention
        fields = ["title", "caught_amount", "details", "hosting_agency", "intervention_photo", "event_date", "volunteer_amount"]
        widgets = {"title": forms.TextInput(attrs = {"class": "form-control",  "id": "interventionTitle", "required": True}), "caught_amount": forms.NumberInput(attrs = {"class": "form-control", "required": "required", "min": 0}), "details": forms.Textarea(attrs = {"class": "form-control", "id": "interventionDetails"}), "hosting_agency": forms.TextInput(attrs = {"class": "form-control", "id": "hostingAgency", "required": "required"}), "intervention_photo": forms.FileInput(attrs = {"class": "form-control", "id": "interventionPhoto", "required": "required"}), "event_date": forms.DateInput(attrs = {"type": "date", "class": "form-control", "id": "interventionDate", "required": "required"}), "volunteer_amount": forms.NumberInput(attrs = {"class": "form-control", "id": "interventionCount", "min": 0})}  
        help_texts = {"title": None, "caught_amount": None, "details": None, "hosting_agency": None, "intervention_photo": None, "event_date": None, "volunteer_amount": None}

    details = forms.CharField(widget = forms.Textarea(attrs = {"class": "form-control"}), required = False)
    volunteer_amount = forms.IntegerField(widget = forms.NumberInput(attrs = {"class": "form-control"}), required = False)
    
    def clean_event_date(self):
        event_date = self.cleaned_data.get("event_date")
        
        if event_date > date.today():
            raise ValidationError("The date cannot be in the future.")
        
        return event_date


class StatusForm(forms.ModelForm):
    required_css_class = "required"
    class Meta:
        model = Status
        fields = ["location", "onset_date", "statustype"]
        widgets = {"onset_date": forms.DateInput(attrs = {"type": "date", "class": "form-control", "required": "required"}), "location": forms.Select(attrs = {"class": "form-control", "required": "required"}), "statustype": forms.Select(attrs = {"class": "form-control", "required": "required"})}
        help_texts = {"onset_date": None, "location": None, "statustype": None,}

    def save(self, commit = True):
        status = super().save(commit = False)

        location = status.location
        
        onset_date = status.onset_date

        latest_status = Status.objects.filter(location = location).order_by("-onset_date").first()

        start_date = latest_status.onset_date if latest_status else datetime.date.min

        interventions = Intervention.objects.filter(location = location, event_date__gt = start_date, event_date__lte = onset_date)
        
        caught_overall = interventions.aggregate(Sum("caught_amount"))["caught_amount__sum"] or 0
        
        volunteer_overall = interventions.aggregate(Sum("volunteer_amount"))["volunteer_amount__sum"] or 0

        status.caught_overall = caught_overall

        status.volunteer_overall = volunteer_overall

        if commit:
            status.save()
        
        return status