from django.db import models
from django.utils import timezone
from artist.models import Artist, Genre

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

    name = models.CharField()
    datetime = models.DateTimeField()
    city = models.CharField()
    city_district = models.CharField()
    address = models.CharField()
    location_name = models.CharField()
    price = models.PositiveIntegerField()
    description = models.TextField()
    is_active = models.BooleanField()
    is_confirmed = models.BooleanField()
    is_hidden = models.BooleanField()
    red = models.PositiveIntegerField()
    green = models.PositiveIntegerField()
    blue = models.PositiveIntegerField()
    time_created = models.DataTimeField()

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
    search_text = models.CharField(max_length=128)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return search_text
