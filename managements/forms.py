from django import forms
from .models import Status, StatusType, Intervention
from django.db.models import Sum
import datetime


class InterventionForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Intervention
        fields = [
            'title',
            'caught_amount',
            'details',
            'hosting_agency',
            'intervention_photo',
            'intervention_date',
            'volunteer_amount'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'caught_amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'hosting_agency': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'intervention_photo': forms.FileInput(attrs={'class': 'form-control', 'id': 'interventionPhoto', 'required': 'required'}),
            'intervention_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'volunteer_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'title': None,
            'caught_amount': None,
            'details': None,
            'hosting_agency': None,
            'intervention_photo': None,
            'intervention_date': None,
            'volunteer_amount': None
        }

    details = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False
    )

    volunteer_amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )

class StatusForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Status
        fields = ['location', 'onset_date', 'statustype']
        widgets = {
            'onset_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'location': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'statustype': forms.Select(attrs={'class': 'form-control', 'required': 'required'})
        }

        help_texts = {
            'onset_date': None,
            'location': None,
            'statustype': None,
        }

    def save(self, commit=True):
        status = super().save(commit=False)
        location = status.location
        onset_date = status.onset_date

        # Get the latest Status for the location
        latest_status = Status.objects.filter(location=location).order_by('-onset_date').first()

        # Determine the start date for summing caught amounts
        start_date = latest_status.onset_date if latest_status else datetime.date.min

        # Sum caught amounts for interventions between the latest onset date and the new onset date
        interventions = Intervention.objects.filter(location=location, intervention_date__gt=start_date, intervention_date__lte=onset_date)
        caught_overall = interventions.aggregate(Sum('caught_amount'))['caught_amount__sum'] or 0
        volunteer_overall = interventions.aggregate(Sum('volunteer_amount'))['volunteer_amount__sum'] or 0

        # Determine the status type based on the new caught_overall
        """ if caught_overall < 100:
            status.statustype = StatusType.objects.get(is_low=True)
        elif 100 <= caught_overall <= 500:
            status.statustype = StatusType.objects.get(is_moderate=True)
        else:
            status.statustype = StatusType.objects.get(is_critical=True) """

        status.caught_overall = caught_overall
        status.volunteer_overall = volunteer_overall

        if commit:
            status.save()
        return status
