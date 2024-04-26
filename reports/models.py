from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import mark_safe
from authentications.models import User
from managements.models import Location

import datetime


# Create your models here.
class PostPhoto(models.Model):
    post_photo = models.ImageField(default = "posts/default.png", null = True, upload_to = "posts", help_text = "Designates the photo of the post.", verbose_name = "Post Photo")
    class Meta:
        db_table = "reports_post_photo"
        verbose_name = "Post Photo"
        verbose_name_plural = "Posts Photos"
    
    def gallery_photo(self):
        if self.post_photo != "":
            return mark_safe("<img src = '%s%s'/>" % (f"{settings.MEDIA_URL}", self.post_photo))
    
    gallery_photo.short_description = "Gallery Photo"
    
    def __str__(self):
        return "PHOTO " + str(self.id)


class Coordinates(models.Model):
    latitude = models.DecimalField(max_digits = 9, decimal_places = 6, help_text = "Designates the latitude of the post.", verbose_name = "Latitude")
    longitude = models.DecimalField(max_digits = 9, decimal_places = 6, help_text = "Designates the longitude of the post.", verbose_name = "Longitude")

    class Meta:
        db_table = "reports_coordinates"
        verbose_name = "Coordinates"
        verbose_name_plural = "Coordinates"
    
    def __str__(self):
        return str(self.latitude) + "° N, " + str(self.longitude) + "° E"

class PostStatus(models.Model):
    is_valid = models.BooleanField(default = False, help_text = "Designates that the post can be pinned into the contributors site.", verbose_name = "Valid")
    is_invalid = models.BooleanField(default = False, help_text = "Designates that the post cannot be pinned into the contributors site.", verbose_name = "Invalid")
    is_pending = models.BooleanField(default = False, help_text = "Designates that the post is under review to be pinned into the contributors site.", verbose_name = "Pending")
    is_draft = models.BooleanField(default = False, help_text = "Designates that the post is under draft to be reviewed for the contributors site.", verbose_name = "Draft")
   
    class Meta:
        db_table = "reports_post_status"
        verbose_name = "Post Status"
        verbose_name_plural = "Posts Status"
    
    def __str__(self):
        if self.is_valid == True:
            return "Valid"
        
        elif self.is_invalid == True:
            return "Invalid"
        
        elif self.is_pending == True:
            return "Pending"
        
        elif self.is_draft == True:
            return "Draft"


class Depth(models.Model):
    is_deep = models.BooleanField(default = False, help_text = "Designates that the depth is deep.", verbose_name = "Deep")
    is_moderate = models.BooleanField(default = False, help_text = "Designates that the depth is moderate.", verbose_name = "Moderate")
    is_shallow = models.BooleanField(default = False, help_text = "Designates that the depth is shallow.", verbose_name = "Shallow")
   
    class Meta:
        db_table = "reports_depth"
        verbose_name = "Depth"
        verbose_name_plural = "Depths"
    
    def __str__(self):
        if self.is_deep == True:
            return "Deep"
        
        elif self.is_moderate == True:
            return "Moderate"
        
        elif self.is_shallow == True:
            return "Shallow"
        
class Weather(models.Model):
    is_sunny = models.BooleanField(default = False, help_text = "Designates that the weather is sunny.", verbose_name = "Sunny")
    is_cloudy = models.BooleanField(default = False, help_text = "Designates that the weather is cloudy.", verbose_name = "Cloudy")
    is_windy = models.BooleanField(default = False, help_text = "Designates that the weather is windy.", verbose_name = "Windy")
    is_rainy = models.BooleanField(default = False, help_text = "Designates that the weather is rainy.", verbose_name = "Rainy")
    is_stormy = models.BooleanField(default = False, help_text = "Designates that the weather is stormy.", verbose_name = "Stormy")
    class Meta:
        db_table = "reports_weather"
        verbose_name = "Weather"
        verbose_name_plural = "Weathers"
    
    def __str__(self):
        if self.is_sunny == True:
            return "Sunny"
        
        elif self.is_cloudy == True:
            return "Cloudy"
        
        elif self.is_windy == True:
            return "Windy"
        
        elif self.is_rainy == True:
            return "Rainy"
        
        elif self.is_stormy == True:
            return "Stormy"

class PostObservation(models.Model):
    size = models.IntegerField(validators = [MinValueValidator(0)], null = True, blank = True, help_text = "Designates the size of the Crown-of-Thorns Starfish at the moment the post taken.", verbose_name = "Size / Centimeter")
    depth = models.ForeignKey(Depth, on_delete = models.CASCADE, null = True, blank = True, help_text = "Designates the foreign key of the Depth model.", verbose_name = "Depth")
    density = models.IntegerField(validators = [MinValueValidator(0)], null = True, blank = True, help_text = "Designates the density of the Crown-of-Thorns Starfish at the moment the post taken.", verbose_name = "Density / Square Meter")
    weather = models.ForeignKey(Weather, on_delete = models.CASCADE, null = True, blank = True, help_text = "Designates the foreign key of the Weather model.", verbose_name = "Weather")

    class Meta:
        db_table = "reports_post_observation"
        verbose_name = "Post Observation"
        verbose_name_plural = "Posts Observations"
    
    def __str__(self):
        return "OBSERVATION " + str(self.id)
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, help_text = "Designates the foreign key of the User model.", verbose_name = "User")
    description = models.TextField(max_length = 1500, help_text = "Designates the description of the post.", verbose_name = "Description")
    capture_date = models.DateTimeField(default = datetime.datetime.now(), help_text = "Designates the capture date and time of the post.", verbose_name = "Capture Date")
    post_photos = models.ManyToManyField(PostPhoto, blank = True, through = "PostGallery", help_text = "Designates the foreign key of the Post Photo model.", verbose_name = "Post Photos")
    coordinates = models.ForeignKey(Coordinates, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Coordinates model.", verbose_name = "Coordinates")
    location = models.ForeignKey(Location, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Location model.", verbose_name = "Location")
    post_status = models.ForeignKey(PostStatus, on_delete = models.CASCADE, default = 4, help_text = "Designates the foreign key of the Post Status model.", verbose_name = "Post Status")
    post_observation = models.ForeignKey(PostObservation, null = True, blank = True, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Post Observation model.", verbose_name = "Post Observation")

    class Meta:
        db_table = "reports_post"
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return "POST " + str(self.id) + " | " + str(self.user)


class PostGallery(models.Model):
    post_photos = models.ForeignKey(PostPhoto, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Post Photos model.", verbose_name = "Post Photo")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Post model.", verbose_name = "Post")

    class Meta:
        db_table = "reports_post_gallery"
        verbose_name = "Post Gallery"
        verbose_name_plural = "Posts Gallery"
    
    def __str__(self):
        return "GALLERY " + str(self.id)