from django.core.exceptions import ObjectDoesNotExist
from task_manager.statuses.models import Status
from django.urls import reverse
from json import load
from task_manager.users.models import CustomUser
from task_manager.tests.test_auth import AuthTestCase
from django.contrib.messages import get_messages
from task_manager.settings import BASE_DIR
from django.utils.translation import gettext_lazy as _


FIXTURES = f'{BASE_DIR}/task_manager/tests/fixtures'


def get_content(filename):
    with open(f'{FIXTURES}/{filename}') as file:
        return load(file)


class StatusesTestCase(AuthTestCase):
    page = 'statuses'

    def setUp(self):
        self.dump_data = get_content('data.json')
        user = self.dump_data.get('users').get('existing1')
        status = self.dump_data.get('statuses').get('existing')
        CustomUser.objects.create(**user)
        Status.objects.create(**status)

    def test_index_page(self):
        # without authorization
        self.client.logout()
        response = self.client.get(reverse('statuses:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(messages[0].message,
                         _('To open this page log in!'))

        # logged in
        self.client.force_login(user=CustomUser.objects.get(id=1))
        response = self.client.get(reverse('statuses:index'))
        self.assertEqual(response.status_code, 200)

        statuses = Status.objects.all()
        count = statuses.count()
        self.assertEqual(count, 1)
        self.assertQuerysetEqual(
            response.context_data['status_list'],
            statuses,
            ordered=False,
        )

    def test_create(self):
        self.client.force_login(user=CustomUser.objects.get(id=1))
        response = self.client.get(reverse('statuses:create'))
        self.assertEqual(response.status_code, 200)

        new_status = self.dump_data.get('statuses').get('new')
        response = self.client.post(reverse('statuses:create'), new_status)
        created_status = Status.objects.get(id=new_status.get('pk'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(created_status.name, new_status.get('name'))
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(messages[0].message, _('Status successfully added!'))

    def test_update(self):
        self.client.force_login(user=CustomUser.objects.get(id=1))
        exist_status = Status.objects.get(pk=1)
        response = self.client.get(reverse('statuses:update',
                                           args=[exist_status.pk]))
        self.assertEqual(response.status_code, 200)

        new_status = self.dump_data.get('statuses').get('updated')
        response = self.client.post(
            reverse('statuses:update', args=[exist_status.pk]),
            new_status,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('statuses:index'))
        updated_status = Status.objects.get(pk=exist_status.pk)
        self.assertEqual(updated_status.name, new_status.get('name'))
        self.assertEqual(messages[0].message, _('Status successfully updated!'))

    def test_delete(self):
        self.client.force_login(user=CustomUser.objects.get(id=1))
        exist_status = Status.objects.get(id=1)
        response = self.client.post(reverse('statuses:delete',
                                            args=[exist_status.pk]))
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(messages[0].message, _('Status successfully deleted!'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=1)
