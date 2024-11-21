from django.conf import settings
from django.db import models

from account.models import User


# Create your models here.

class Anime(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.JSONField()  # Allows storing a list of strings
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes
    thumbnail = models.ImageField(upload_to="media/")  # Corrected upload_to
    video_url = models.URLField()
    reviews = models.ManyToManyField(
        'Review',  # Assuming a separate Review model exists
        blank=True,
        related_name='related_anime'  # Unique related_name
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    anime = models.ForeignKey(
        Anime,  # ForeignKey to Anime
        on_delete=models.CASCADE,
        related_name='anime_reviews'  # Unique related_name for reverse relationship
    )
    user = models.ForeignKey(
        User,  # Linking to the custom User model
        on_delete=models.CASCADE,
        related_name='user_reviews'  # Unique related_name for reverse relationship
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatica


class UserAnimeList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='anime_lists'
    )
    anime = models.ForeignKey(
        'Anime',
        on_delete=models.CASCADE,
        related_name='user_lists'
    )
    added_at = models.DateTimeField(auto_now_add=True)  # When the anime was added to the list

    class Meta:
        unique_together = ('user', 'anime')  # Prevent duplicate entries for the same user and anime
