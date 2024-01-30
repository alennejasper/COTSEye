from django.db import models
from authentications.models import User


# Create your models here.
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True, help_text = "Designates the foreign key of the User model.", verbose_name = "User")
    title = models.CharField(max_length = 150, help_text = "Designates the title of the announcement.", verbose_name = "Title")
    context = models.TextField(max_length = 5000, null = True, help_text = "Designates the context of the announcement.", verbose_name = "Context")
    place = models.CharField(max_length = 150, help_text = "Designates the place of the announcement.", verbose_name = "Place")
    release_date = models.DateTimeField(auto_now_add = True, help_text = "Designates the release date and time of the announcement.", verbose_name = "Release Date")
    announcement_photo = models.ImageField(default = "announcements/default.png", null = True, blank = True, upload_to = "announcements", help_text = "Designates the photo of the announcement.", verbose_name = "Announcement Photo")

    release_date.editable = True

    class Meta:
            db_table = "auxiliaries_announcement"
            verbose_name = "Announcement"
            verbose_name_plural = "Announcements"
    
    def __str__(self):
        return str(self.title) + " | " + str(self.user)