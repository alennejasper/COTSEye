from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
from .models import Status, StatusType, Intervention

import datetime


def validate_not_future_date(value):
    if value > date.today():
        raise ValidationError("The date cannot be in the future.")
    
class InterventionForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Intervention
        fields = ["title", "caught_amount", "details", "hosting_agency", "intervention_photo", "intervention_date", "volunteer_amount"]
        widgets = {"title": forms.TextInput(attrs = {"class": "form-control", "required": "required"}), "caught_amount": forms.NumberInput(attrs = {"class": "form-control", "required": "required", "min": 0}), "details": forms.Textarea(attrs = {"class": "form-control"}), "hosting_agency": forms.TextInput(attrs = {"class": "form-control", "required": "required"}), "intervention_photo": forms.FileInput(attrs = {"class": "form-control", "id": "interventionPhoto", "required": "required"}), "intervention_date": forms.DateInput(attrs = {"type": "date", "class": "form-control", "required": "required"}), "volunteer_amount": forms.NumberInput(attrs = {"class": "form-control", "min": 0})}  
        help_texts = {"title": None, "caught_amount": None, "details": None, "hosting_agency": None, "intervention_photo": None, "intervention_date": None, "volunteer_amount": None}

    details = forms.CharField(widget = forms.Textarea(attrs = {"class": "form-control"}), required = False)
    volunteer_amount = forms.IntegerField(widget = forms.NumberInput(attrs = {"class": "form-control"}), required = False)
    
    def clean_intervention_date(self):
        intervention_date = self.cleaned_data.get("intervention_date")
        
        if intervention_date > date.today():
            raise ValidationError("The date cannot be in the future.")
        
        return intervention_date

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

        interventions = Intervention.objects.filter(location = location, intervention_date__gt = start_date, intervention_date__lte = onset_date)
        
        caught_overall = interventions.aggregate(Sum("caught_amount"))["caught_amount__sum"] or 0
        
        volunteer_overall = interventions.aggregate(Sum("volunteer_amount"))["volunteer_amount__sum"] or 0

        status.caught_overall = caught_overall

        status.volunteer_overall = volunteer_overall

        if commit:
            status.save()
        
        return status