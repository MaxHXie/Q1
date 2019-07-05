from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    name = models.CharField(max_length=64, blank=True)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(max_length=64, blank=True)
    telephone = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=64, blank=True)
    city_district = models.CharField(max_length=64, blank=True)
    description = models.TextField(max_length=2048, blank=True)
    gender = models.CharField(max_length=1,
                            choices = (
                                ('N', 'No answer'),
                                ('M', 'Male'),
                                ('F', 'Female'),
                                ('O', 'Other')
                            ), default="N"
                            )
    profile_picture = models.ImageField(upload_to="profile_picture", blank=True)
    valid_profile = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    accepted_terms = models.BooleanField(default=False)

    def __str__(self):
        try:
            string = "%s %s" % (self.first_name, self.last_name)
        except:
            string = "Error"
        return string

class Fan(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    telephone = models.CharField(max_length=16)
    gender = models.CharField(max_length=1,
                            choices=(
                                ('N', 'No answer'),
                                ('M', 'Male'),
                                ('F', 'Female'),
                                ('O', 'Other')
                            ), default="N"
                            )
    profile_picture = models.ImageField(upload_to="profile_picture")
    valid_profile = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    accepted_terms = models.BooleanField(default=True)

    def __str__(self):
        try:
            string = "%s %s" % (self.first_name, self.last_name)
        except:
            string = "Error"
        return string

class Boost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    artist = models.ForeignKey(
        Artist,
        on_delete = models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete = models.CASCADE
    )
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user == None:
            string = "Unknown user visited %s" % (self.artist.name)
        else:
            string = "%s visited %s" % (self.user.email, self.artist.name)
        return string

class Follow(models.Model):
    artist = models.ForeignKey(
        Artist,
        on_delete = models.CASCADE
    )
    follower = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('artist', 'follower')

class Visit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    artist = models.ForeignKey(
        Artist,
        on_delete = models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete = models.CASCADE
    )
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user == None:
            string = "Unknown user visited %s" % (self.artist.name)
        else:
            string = "%s visited %s" % (self.user.email, self.artist.name)
        return string
