from django.forms import ModelForm
from django.forms.widgets import FileInput
from .models import Coordinates, PostObservation, Post
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

class CoordinatesForm(ModelForm):
    class Meta:
        model = Coordinates
        fields = "__all__"


class PostObservationForm(ModelForm):
    class Meta:
        model = PostObservation
        fields = "__all__"


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["user", "coordinates", "post_status", "post_observation", "creation_date"]
        widgets = {"post_photo": FileInput()}

    def clean_capture_date(self):
        capture_date = self.cleaned_data.get("capture_date")

        if capture_date:
            if capture_date.tzinfo is not None:
                capture_date = capture_date.replace(tzinfo = None)
            
            current_date = datetime.now()

            if (current_date - capture_date).days > 7:
                raise ValidationError("The capture date cannot be more than 7 days from the current one.")
            
        return capture_date