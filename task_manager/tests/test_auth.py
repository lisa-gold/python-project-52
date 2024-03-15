from django.test import TestCase
from django.urls import reverse
from json import load
from django.contrib.messages import get_messages
from task_manager.settings import BASE_DIR
from django.utils.translation import gettext_lazy as _


FIXTURES = f'{BASE_DIR}/task_manager/tests/fixtures'


def get_content(filename):
    with open(f'{FIXTURES}/{filename}') as file:
        return load(file)


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
