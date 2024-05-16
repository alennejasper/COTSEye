from django import forms
from authentications.models import User
from auxiliaries.models import Announcement

class AnnouncementForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'announcementUser', 'required': True}),
        help_text="Designates the foreign key of the User model.",
        label="User"
    )

    class Meta:
        model = Announcement
        fields = [
            'title',
            'release_date',
            'place',
            'context',
            'user',
            'announcement_photo',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'announcementTitle', 'required': True}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'announcementDate', 'type': 'date', 'required': True}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'id': 'announcementLocation', 'required': True}),
            'context': forms.Textarea(attrs={'class': 'form-control', 'id': 'announcementDescription', 'rows': 3, 'required': True}),
            'announcement_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'announcementPhoto'}),
        }