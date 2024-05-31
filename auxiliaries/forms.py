from django import forms
from authentications.models import User
from auxiliaries.models import Announcement
from managements.models import Location

class AnnouncementForm(forms.ModelForm):
    required_css_class = 'required'
    
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-control", "id": "announcementUser", "required": True}),
        label="User"
    )

    class Meta:
        model = Announcement
        fields = ["title", "release_date", "context", "user", "announcement_photo"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "id": "announcementTitle", "required": True}),
            "release_date": forms.DateInput(attrs={"class": "form-control", "id": "announcementDate", "type": "date", "required": True}),
            "context": forms.Textarea(attrs={"class": "form-control", "id": "announcementDescription", "rows": 3, "required": True}),
            "announcement_photo": forms.FileInput(attrs={"class": "form-control-file", "id": "announcementPhoto"})
        }

        help_texts = {
            'title': None,
            'release_date': None,
            'context': None,
            'announcement_photo': None
        }

