from django.test import SimpleTestCase
from django.urls import resolve, reverse
from events.views import index, create, confirm, single, all_events, edit, my_events, participants, hide_show, signup

class TestUrls(SimpleTestCase):

    '''
    Unit test for all paths in urls.py and corresponding view
    '''

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_create_url_resolves(self):
        url = reverse('create_event')
        self.assertEquals(resolve(url).func, create)

    def test_confirm_url_resolves(self):
        url = reverse('confirm', kwargs={'id':1})
        self.assertEquals(resolve(url).func, confirm)

    def test_single_url_resolves(self):
        url = reverse('single', kwargs={'id':1})
        self.assertEquals(resolve(url).func, single)

    def test_all_events_url_resolves(self):
        url = reverse('all_events')
        self.assertEquals(resolve(url).func, all_events)

    def test_edit_url_resolves(self):
        url = reverse('edit', kwargs={'id':1})
        self.assertEquals(resolve(url).func, edit)

    def test_my_events_url_resolves(self):
        url = reverse('my_events')
        self.assertEquals(resolve(url).func, my_events)

    def test_participants_url_resolves(self):
        url = reverse('participants', kwargs={'id':1})
        self.assertEquals(resolve(url).func, participants)

    def test_hide_show_url_resolves(self):
        url = reverse('hide_show', kwargs={'id':1})
        self.assertEquals(resolve(url).func, hide_show)

    def test_signup_url_resolves(self):
        url = reverse('signup', kwargs={'id':1})
        self.assertEquals(resolve(url).func, signup)
