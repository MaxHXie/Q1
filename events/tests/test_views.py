from django.test import TestCase, Client
from django.urls import reverse
from events.models import Event, Signup, Search
import json

class TestViews(TestCase):
    '''
    Test each view and their corresponding html template

    Want to test unique user stories
        Example:
            Logging in
            Creating event -> Rejected, Needs to complete profile
            Edit profile
            Creating event
            See my finished event
            See participants
        etc.
    '''

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.create_url = reverse('create_event')
        self.confirm_url = reverse('confirm', kwargs={'id': 1})
        self.single_url = reverse('single', kwargs={'id': 1})
        self.all_events_url = reverse('all_events')
        self.my_events_url = reverse('my_events')
        self.edit_url = reverse('edit', kwargs={'id': 1})
        self.participants_url = reverse('participants', kwargs={'id': 1})
        self.hide_show_url = reverse('hide_show', kwargs={'id': 1})
        self.signup_url = reverse('signup', kwargs={'id': 1})

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        self.assertTemplateUsed(response, 'html_parts/footer.html')

        self.assertTemplateNotUsed(response, 'events_page.html')

    def test_create_GET(self):
        response = self.client.get(self.create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events_page.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        self.assertTemplateUsed(response, 'html_parts/footer.html')

        self.assertTemplateNotUsed(response, 'landing_page.html')

    def test_confirm_GET(self):
        response = self.client.get(self.confirm_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events_page.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        self.assertTemplateUsed(response, 'html_parts/footer.html')

        self.assertTemplateNotUsed(response, 'landing_page.html')


    def test_single_GET(self):
        response = self.client.get(self.single_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events_page.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        self.assertTemplateUsed(response, 'html_parts/footer.html')

        self.assertTemplateNotUsed(response, 'landing_page.html')

    def test_all_events_GET(self):
        response = self.client.get(self.all_events_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events_page.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        self.assertTemplateUsed(response, 'html_parts/footer.html')

        self.assertTemplateNotUsed(response, 'landing_page.html')

    def test_my_events_GET(self):
        response = self.client.get(self.my_events_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events_page.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        self.assertTemplateUsed(response, 'html_parts/footer.html')

        self.assertTemplateNotUsed(response, 'landing_page.html')

    def test_edit_GET(self):
        response = self.client.get(self.edit_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events_page.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        self.assertTemplateUsed(response, 'html_parts/footer.html')

        self.assertTemplateNotUsed(response, 'landing_page.html')

    def test_participants_GET(self):
        response = self.client.get(self.participants_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events_page.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        self.assertTemplateUsed(response, 'html_parts/footer.html')

        self.assertTemplateNotUsed(response, 'landing_page.html')

    def test_hide_show_GET(self):
        response = self.client.get(self.hide_show_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events_page.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        self.assertTemplateUsed(response, 'html_parts/footer.html')

        self.assertTemplateNotUsed(response, 'landing_page.html')

    # def test_signup_GET(self):
        # METHOD IN VIEWS IS NOT DONE YET
        #
        # response = self.client.get(self.signup_url)
        #
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'events_page.html')
        # self.assertTemplateUsed(response, 'base.html')
        # self.assertTemplateUsed(response, 'html_parts/navbar1.html')
        # self.assertTemplateUsed(response, 'html_parts/message_banner.html')
        # self.assertTemplateUsed(response, 'html_parts/footer.html')
        #
        # self.assertTemplateNotUsed(response, 'landing_page.html')
