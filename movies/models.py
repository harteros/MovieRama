from django.conf import settings
from django.db import models


# Create your models here.

class Movie(models.Model):
    """
        Stores a single movie, related to :model:`auth.User`.
    """
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )
    pub_date = models.DateTimeField('date published')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_likes", blank=True)
    hates = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_hates", blank=True)

    def __str__(self):
        """
            Returns a movie by its title
        """
        return self.title
