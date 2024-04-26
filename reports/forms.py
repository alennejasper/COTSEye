from django.forms import ModelForm
from django.forms.widgets import FileInput
from .models import Coordinates, PostObservation, Post


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
        exclude = ["user", "coordinates", "location", "post_status", "post_observation"]
        widgets = {"post_photo": FileInput()}