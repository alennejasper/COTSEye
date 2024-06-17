from django import forms
from auxiliaries.models import Announcement

class AnnouncementForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Announcement
        fields = ["title", "release_date", "context", "hosting_agency", "announcement_photo"]
        widgets = {"title": forms.TextInput(attrs = {"class": "form-control", "id": "announcementTitle", "required": True}), "release_date": forms.DateInput(attrs = {"class": "form-control", "id": "announcementDate", "type": "date", "required": True}), "context": forms.Textarea(attrs = {"class": "form-control", "id": "announcementDescription", "rows": 3, "required": True}), "announcement_photo": forms.FileInput(attrs = {"class": "form-control-file", "id": "announcementPhoto"}),"hos ting_agency": forms.TextInput(attrs = {"class": "form-control", "id": "hostingAgency", "required": True})}
        help_texts = {"title": None, "release_date": None, "context": None, "announcement_photo": None}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

    def save(self, commit = True):
        instance = super().save(commit = False)
 
        if self.user:
            instance.user = self.user

        if commit:
            instance.save()

        return instance