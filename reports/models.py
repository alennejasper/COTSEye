from django.db import models
from authentications.models import User

import datetime


# Create your models here.
class Coordinates(models.Model):
    latitude = models.DecimalField(null = True, max_digits = 9, decimal_places = 6, help_text = "Designates the latitude of the post.", verbose_name = "Latitude")
    longitude = models.DecimalField(null = True, max_digits = 9, decimal_places = 6, help_text = "Designates the longitude of the post.", verbose_name = "Longitude")

    class Meta:
        db_table = "reports_coordinates"
        verbose_name = "Coordinates"
        verbose_name_plural = "Coordinates"
    
    def __str__(self):
        return str(self.latitude) + "° N, " + str(self.longitude) + "° E"

class PostStatus(models.Model):
    is_valid = models.BooleanField(default = False, help_text = "Designates that the post can be pinned into the contributors site.", verbose_name = "Valid Status")
    is_invalid = models.BooleanField(default = False, help_text = "Designates that the post cannot be pinned into the contributors site.", verbose_name = "Invalid Status")
    is_uncertain = models.BooleanField(default = False, help_text = "Designates that the post is under review to be pinned into the contributors site.", verbose_name = "Uncertain Status")
   
    class Meta:
        db_table = "reports_post_status"
        verbose_name = "Post Status"
        verbose_name_plural = "Posts Status"
    
    def __str__(self):
        if self.is_valid == True:
            return "Valid"
        
        elif self.is_invalid == True:
            return "Invalid"
        
        elif self.is_uncertain == True:
            return "Uncertain"

class PostObservations(models.Model):
    size = models.CharField(max_length = 150, null = True, blank = True, help_text = "Designates the size of the Crown-of-Thorns Starfish at the moment the post taken.", verbose_name = "Size")
    depth = models.CharField(max_length = 150, null = True, blank = True, help_text = "Designates the depth of the Crown-of-Thorns Starfish at the moment the post taken.", verbose_name = "Depth")
    density = models.CharField(max_length = 150, null = True, blank = True, help_text = "Designates the density of the Crown-of-Thorns Starfish at the moment the post taken.", verbose_name = "Density")
    weather = models.CharField(max_length = 150, null = True, blank = True, help_text = "Designates the weather at the moment the post taken.", verbose_name = "Weather")

    class Meta:
        db_table = "reports_post_observations"
        verbose_name = "Post Observations"
        verbose_name_plural = "Posts Observations"
    
    def __str__(self):
        return "OBSV " + str(self.id)
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True, help_text = "Designates the foreign field of the User model.", verbose_name = "User")
    description = models.TextField(max_length = 1500, null = True, blank = True, help_text = "Designates the description of the post.", verbose_name = "Description")
    capture_date = models.DateTimeField(default = datetime.datetime.now(), help_text = "Designates the capture date and time of the post.", verbose_name = "Capture Date")
    post_photo = models.ImageField(default = "posts/default.png", null = True, blank = True, upload_to = "posts", help_text = "Designates the photo of the post.", verbose_name = "Post Photo")
    coordinates = models.ForeignKey(Coordinates, on_delete = models.CASCADE, null = True, blank = True, help_text = "Designates the foreign field of the Coordinates model.", verbose_name = "Coordinates")
    post_status = models.ForeignKey(PostStatus, on_delete = models.CASCADE, default = 1, null = True, blank = True, help_text = "Designates the foreign field of the Post Status model.", verbose_name = "Post Status")
    post_observations = models.ForeignKey(PostObservations, on_delete = models.CASCADE, null = True, blank = True, help_text = "Designates the foreign field of the Post Observations model.", verbose_name = "Post Observations")

    class Meta:
        db_table = "reports_post"
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return "POST " + str(self.id) + " | " + str(self.user)