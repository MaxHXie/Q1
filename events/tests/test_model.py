from django.test import TestCase
from django.utils import timezone
from events.models import Event, Signup, Search
from users.models import Artist, Genre
from django.contrib.auth.models import User

class TestModels(TestCase):

    def setUp(self):
        self.datetime = timezone.now()
        user = User.objects.create_user('Kalle', 'kalle@anka.com', 'superkalle')
        genre = Genre.objects.create()
        genre.name  = 'Dansband'
        genre.save()
        self.artist = Artist.objects.create(
            user = user,
            name = 'Koola Kalle',
            first_name = 'Kalle',
            last_name = 'Kula',
            genres = genre,
            email = 'kalle@anka.com',
            telephone = '0711231212',
            city = 'Kiruna',
            city_district = 'Kiruna',
            description = 'Super kula super coola Kalle',
            gender = 'M'
        )
        self.event = Event.objects.create(
            artist = self.artist,
            genre  = genre,
            name = 'The party',
            datetime = self.datetime,
            city = 'Stockholm',
            city_district = 'Stockholm',
            address = 'Sveavägen',
            location_name = 'Blubb klå',
            price = 100,
            description = 'Super kula super coola Kalle partyt'
        )

    def test_return_string(self):
        self.assertEquals(str(self.event), 'The party by Kalle Kula')

    def test_has_happened(self):
        self.assertTrue(self.event.has_happened)
        self.event.datetime = self.datetime + timezone.timedelta(days=365)
        self.event.save()
        self.assertFalse(self.event.has_happened)
