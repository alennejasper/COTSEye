from django.forms import ModelForm
from django.forms.widgets import FileInput
from .models import Coordinates, PostObservations, Post


class CoordinatesForm(ModelForm):
    class Meta:
        model = Coordinates
        fields = "__all__"


class PostObservationsForm(ModelForm):
    class Meta:
        model = PostObservations
        fields = "__all__"


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["user", "coordinates", "post_status", "post_observations"]
        widgets = {"post_photo": FileInput()}