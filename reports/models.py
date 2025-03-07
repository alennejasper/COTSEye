from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import mark_safe
from authentications.models import User
from managements.models import Location

import datetime


# Create your models here.
class PostPhoto(models.Model):
    post_photo = models.ImageField(default = "posts/default.png", null = True, upload_to = "posts", verbose_name = "Post Photo")
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
    latitude = models.DecimalField(max_digits = 9, decimal_places = 6, verbose_name = "Latitude")
    longitude = models.DecimalField(max_digits = 9, decimal_places = 6, verbose_name = "Longitude")

    class Meta:
        db_table = "reports_coordinates"
        verbose_name = "Coordinates"
        verbose_name_plural = "Coordinates"
    
    def __str__(self):
        return str(self.latitude) + "° N, " + str(self.longitude) + "° E"

class PostStatus(models.Model):
    is_valid = models.BooleanField(default = False, verbose_name = "Valid")
    is_invalid = models.BooleanField(default = False, verbose_name = "Invalid")
    is_pending = models.BooleanField(default = False, verbose_name = "Pending")
    is_draft = models.BooleanField(default = False, verbose_name = "Draft")
   
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


class Size(models.Model):
    size = models.CharField(max_length = 65, unique = True, error_messages = {"unique": "This size already exist."}, null = True, verbose_name = "Size")
    description = models.TextField(max_length = 255, verbose_name = "Description")
    
    class Meta:
        db_table = "reports_size"
        verbose_name = "Size"
        verbose_name_plural = "Size"
    
    def __str__(self):
        return str(self.size) + " (" + str(self.description) + ") " 
        
        
class Depth(models.Model):
    depth = models.CharField(max_length = 65, unique = True, error_messages = {"unique": "This depth already exist."}, null = True, verbose_name = "Depth")
    description = models.TextField(max_length = 255, verbose_name = "Description")
    
    class Meta:
        db_table = "reports_depth"
        verbose_name = "Depth"
        verbose_name_plural = "Depth"
    
    def __str__(self):
        return str(self.depth)  + " (" + str(self.description) + ") " 
        

class Density(models.Model):
    density = models.CharField(max_length = 65, unique = True, error_messages = {"unique": "This Density already exist."}, null = True, verbose_name = "Density")
    description = models.TextField(max_length = 255, verbose_name = "Description")
    
    class Meta:
        db_table = "reports_density"
        verbose_name = "Density"
        verbose_name_plural = "Density"
    
    def __str__(self):
        return str(self.density) + " (" + str(self.description) + ") " 


class PostObservation(models.Model):
    size = models.ForeignKey(Size, on_delete = models.CASCADE, null = True, blank = True, verbose_name = "Size")
    depth = models.ForeignKey(Depth, on_delete = models.CASCADE, null = True, blank = True, verbose_name = "Depth")
    density = models.ForeignKey(Density, on_delete = models.CASCADE, null = True, blank = True, verbose_name = "Density")
    weather = models.CharField(max_length = 65, null = True, blank = True, verbose_name = "Weather")

    class Meta:
        db_table = "reports_post_observation"
        verbose_name = "Post Observation"
        verbose_name_plural = "Posts Observations"
    
    def __str__(self):
        return "OBSERVATION " + str(self.id)
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "User")
    validator = models.ForeignKey(User, null = True, blank = True, on_delete = models.SET_NULL, related_name = "validator", verbose_name = "Validator")
    description = models.TextField(max_length = 255, verbose_name = "Description")
    coordinates = models.ForeignKey(Coordinates, on_delete = models.CASCADE, verbose_name = "Coordinates")
    location = models.ForeignKey(Location, blank = True, on_delete = models.CASCADE, verbose_name = "Location")
    post_status = models.ForeignKey(PostStatus, on_delete = models.CASCADE, default = 4, verbose_name = "Post Status")
    post_observation = models.ForeignKey(PostObservation, null = True, blank = True, on_delete = models.CASCADE, verbose_name = "Post Observation")
    remarks = models.CharField(null = True, blank = True, max_length = 255, verbose_name = "Remarks")
    post_photos = models.ManyToManyField(PostPhoto, blank = True, through = "PostGallery", verbose_name = "Post Photos")
    capture_date = models.DateTimeField(default = datetime.datetime.now, verbose_name = "Capture Date")
    creation_date = models.DateTimeField(default = datetime.datetime.now, verbose_name = "Creation Date")

    class Meta:
        db_table = "reports_post"
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return "POST " + str(self.id) + " | " + str(self.user)

    @property
    def is_validated(self):
        return self.validator is not None

class PostGallery(models.Model):
    post_photos = models.ForeignKey(PostPhoto, on_delete = models.CASCADE, verbose_name = "Post Photo")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name = "Post")

    class Meta:
        db_table = "reports_post_gallery"
        verbose_name = "Post Gallery"
        verbose_name_plural = "Posts Gallery"
    
    def __str__(self):
        return "GALLERY " + str(self.id)