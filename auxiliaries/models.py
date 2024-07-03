from django.db import models

import datetime


# Create your models here.
class File(models.Model):
    author = models.CharField(null = True, max_length = 150, verbose_name = "Author")
    title = models.CharField(max_length = 150, verbose_name = "Title")
    resource_file = models.FileField(upload_to = "resources", verbose_name = "Resource File")
    release_date = models.DateTimeField(default = datetime.datetime.now, verbose_name = "Release Date")

    class Meta:
            db_table = "auxiliaries_file"
            verbose_name = "Resource File"
            verbose_name_plural = "Resource File"
    
    def __str__(self):
        return str(self.title) + " (" + str(self.author) + ") " 


class Inquiry(models.Model):
    question = models.CharField(max_length = 150, verbose_name = "Question")
    answer = models.TextField(max_length = 5000, verbose_name = "Answer")

    class Meta:
            db_table = "auxiliaries_inquiry"
            verbose_name = "FAQ"
            verbose_name_plural = "FAQ"
    
    def __str__(self):
        return str(self.question)
    
    
class Link(models.Model):
    author = models.CharField(null = True, max_length = 150, verbose_name = "Author")
    title = models.CharField(max_length = 150, verbose_name = "Title")
    resource_link = models.CharField(max_length = 2050, verbose_name = "Resource Link")
    release_date = models.DateTimeField(default = datetime.datetime.now, verbose_name = "Release Date")

    class Meta:
            db_table = "auxiliaries_link"
            verbose_name = "Resource Link"
            verbose_name_plural = "Resource Link"
    
    def __str__(self):
        return str(self.title) + " (" + str(self.author) + ") " 
