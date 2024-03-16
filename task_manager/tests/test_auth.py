from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _


class AuthTestCase(TestCase):
    page = 'tasks'

    def test_auth(self):
        # redirect to login page if no authorization
        self.client.logout()
        response = self.client.get(reverse(f'{self.page}:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(messages[0].message,
                         _('To open this page log in!'))
