from django.conf import settings
from django.utils.html import mark_safe
from django.db import models
from authentications.models import User
from managements.models import Location

import datetime


# Create your models here.
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, help_text = "Designates the foreign key of the User model.", verbose_name = "User")
    hosting_agency = models.CharField(null=True, blank=True, max_length = 150, help_text = "Designates the name of the hosting agency.", verbose_name = "Hosting Agency")
    title = models.CharField(max_length = 150, help_text = "Designates the title of the announcement.", verbose_name = "Title")
    context = models.TextField(max_length = 5000, help_text = "Designates the context of the announcement.", verbose_name = "Context")
    location = models.ForeignKey(Location, null = True, blank = True, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Location model.", verbose_name = "Location")
    release_date = models.DateTimeField(default = datetime.datetime.now, help_text = "Designates the release date and time of the announcement.", verbose_name = "Release Date")
    announcement_photo = models.ImageField(default = "announcements/default.png", null = True, upload_to = "announcements", help_text = "Designates the photo of the announcement.", verbose_name = "Announcement Photo")
    creation_date = models.DateTimeField(default = datetime.datetime.now, help_text = "Designates the creation date and time of the announcement.", verbose_name = "Creation Date")

    class Meta:
        db_table = "auxiliaries_announcement"
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def gallery_photo(self):
        if self.announcement_photo != "":
            return mark_safe("<img src = '%s%s'/>" % (f"{settings.MEDIA_URL}", self.announcement_photo))
    
    gallery_photo.short_description = "Gallery Photo"
    
    def get_photo_url(self):
        if self.announcement_photo and hasattr(self.announcement_photo, 'url'):
            return self.announcement_photo.url
        else:
            return settings.MEDIA_URL + "announcements/default.png"
        
    def __str__(self):
        return str(self.title) + " | " + str(self.user) + str(self.announcement_photo.url)

    
class File(models.Model):
    title = models.CharField(max_length = 150, help_text = "Designates the title of the resource file.", verbose_name = "Title")
    author = models.CharField(null=True, max_length = 150, help_text = "Designates the name of the author.", verbose_name = "Author")
    resource_file = models.FileField(upload_to = "resources", help_text = "Designates the file of the resource.", verbose_name = "Resource File")
    release_date = models.DateTimeField(default = datetime.datetime.now, help_text = "Designates the release date and time of the resource file.", verbose_name = "Release Date")

    class Meta:
            db_table = "auxiliaries_file"
            verbose_name = "Resource File"
            verbose_name_plural = "Resource File"
    
    def __str__(self):
        return "FILE " + str(self.id)


class Inquiry(models.Model):
    question = models.CharField(max_length = 150, help_text = "Designates the question of the inquiry.", verbose_name = "Question")
    answer = models.TextField(max_length = 5000, help_text = "Designates the answer of the inquiry.", verbose_name = "Answer")

    class Meta:
            db_table = "auxiliaries_inquiry"
            verbose_name = "FAQ"
            verbose_name_plural = "FAQ"
    
    def __str__(self):
        return str(self.question)
    
    
class Link(models.Model):
    title = models.CharField(max_length = 150, help_text = "Designates the title of the resource link.", verbose_name = "Title")
    author = models.CharField(null=True, max_length = 150, help_text = "Designates the name of the author.", verbose_name = "Author")
    resource_link = models.CharField(max_length = 2050, help_text = "Designates the link of the resource.", verbose_name = "Resource Link")
    release_date = models.DateTimeField(default = datetime.datetime.now, help_text = "Designates the release date and time of the resource link.", verbose_name = "Release Date")

    class Meta:
            db_table = "auxiliaries_link"
            verbose_name = "Resource Link"
            verbose_name_plural = "Resource Link"
    
    def __str__(self):
        return "LINK " + str(self.id)
