from django.db import models
from django.utils import timezone
from users.models import Artist, Genre
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    artist = models.ForeignKey(
        Artist,
        on_delete = models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete = models.CASCADE
    )

    name = models.CharField(max_length=128, blank=True)
    datetime = models.DateTimeField(null=True)
    city = models.CharField(max_length=64, blank=True)
    city_district = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=64, blank=True)
    location_name = models.CharField(max_length=64, blank=True)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=2048, blank=True)
    is_active = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    red = models.PositiveIntegerField(default=255)
    green = models.PositiveIntegerField(default=255)
    blue = models.PositiveIntegerField(default=255)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s by %s %s" % (self.name, self.artist.first_name, self.artist.last_name)

    @property
    def has_happened(self):
        '''
        RETURNS
            Boolean. True if the datetime of the event has passed, otherwise False.
        '''
        return timezone.now() > self.datetime

class Signup(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        null = True
    )
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    telephone = models.CharField(max_length=64)
    is_success = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s signed up to %s" % (self.first_name, self.last_name, self.event.name)

class Search(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        null = True
    )
    search_text = models.CharField(max_length=128)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return search_text
