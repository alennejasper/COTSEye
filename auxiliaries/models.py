from django.db import models
from authentications.models import User

import datetime


# Create your models here.
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, help_text = "Designates the foreign key of the User model.", verbose_name = "User")
    title = models.CharField(max_length = 150, help_text = "Designates the title of the announcement.", verbose_name = "Title")
    context = models.TextField(max_length = 5000, help_text = "Designates the context of the announcement.", verbose_name = "Context")
    place = models.CharField(max_length = 150, help_text = "Designates the place of the announcement.", verbose_name = "Place")
    release_date = models.DateTimeField(default = datetime.datetime.now, help_text = "Designates the release date and time of the announcement.", verbose_name = "Release Date")
    announcement_photo = models.ImageField(default = "announcements/default.png", null = True, blank = True, upload_to = "announcements", help_text = "Designates the photo of the announcement.", verbose_name = "Announcement Photo")

    class Meta:
            db_table = "auxiliaries_announcement"
            verbose_name = "Announcement"
            verbose_name_plural = "Announcements"
    
    def __str__(self):
        return str(self.title) + " | " + str(self.user)


class Resource(models.Model):
    author = models.CharField(max_length = 150, help_text = "Designates the name of the author.", verbose_name = "Author")
    title = models.CharField(max_length = 150, help_text = "Designates the title of the resource.", verbose_name = "Title")
    release_date = models.DateTimeField(default = datetime.datetime.now, help_text = "Designates the release date and time of the resource.", verbose_name = "Release Date")

    class Meta:
            db_table = "auxiliaries_resource"
            verbose_name = "Resource"
            verbose_name_plural = "Resources"
    
    def __str__(self):
        return str(self.title) + " | " + str(self.author)
    
    
class ResourceFile(models.Model):
    resource = models.ForeignKey(Resource, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Resource model.", verbose_name = "Resource")
    resource_file = models.FileField(upload_to = "resources", help_text = "Designates the file of the resource.", verbose_name = "Resource File")

    class Meta:
            db_table = "auxiliaries_resource_file"
            verbose_name = "Resource File"
            verbose_name_plural = "Resource Files"
    
    def __str__(self):
        return "FILE " + str(self.id)

class ResourceLink(models.Model):
    resource = models.ForeignKey(Resource, on_delete = models.CASCADE, help_text = "Designates the foreign key of the Resource model.", verbose_name = "Resource")
    resource_link = models.CharField(max_length = 2050, help_text = "Designates the link of the resource.", verbose_name = "Resource Link")

    class Meta:
            db_table = "auxiliaries_resource_link"
            verbose_name = "Resource Link"
            verbose_name_plural = "Resource Links"
    
    def __str__(self):
        return "LINK " + str(self.id)