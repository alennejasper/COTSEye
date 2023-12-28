from django.db import models
from authentications.models import User


# Create your models here.
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True, help_text = "Designates the foreign field of the User model.", verbose_name = "User")
    title = models.CharField(max_length = 150, help_text = "Designates the title of the announcement.", verbose_name = "Title")
    context = models.TextField(max_length = 5000, null = True, help_text = "Designates the context of the announcement.", verbose_name = "Context")
    place = models.CharField(max_length = 150, help_text = "Designates the place of the announcement.", verbose_name = "Place")
    date = models.DateTimeField(auto_now_add = True, help_text = "Designates the date and time of the post.", verbose_name = "Date")

    date.editable = True

    class Meta:
            db_table = "auxiliaries_announcement"
            verbose_name = "Announcement"
            verbose_name_plural = "Announcements"
    
    def __str__(self):
        return str(self.title) + " | " + str(self.user)