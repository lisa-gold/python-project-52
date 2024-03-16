from django.core.exceptions import ObjectDoesNotExist
from task_manager.statuses.models import Status
from django.urls import reverse
from task_manager.users.models import CustomUser
from task_manager.tests.test_auth import AuthTestCase
from django.contrib.messages import get_messages
from task_manager.tests.parser import get_content
from django.utils.translation import gettext_lazy as _


class StatusesTestCase(AuthTestCase):
    fixtures = ['db.json']
    page = 'statuses'

    def setUp(self):
        self.dump_data = get_content('data.json')
        self.client.force_login(user=CustomUser.objects.get(id=1))

    def test_index_page(self):
        self.client.force_login(user=CustomUser.objects.get(id=1))
        response = self.client.get(reverse('statuses:index'))
        self.assertEqual(response.status_code, 200)

        statuses = Status.objects.all()
        count = statuses.count()
        self.assertEqual(count, 2)
        self.assertQuerysetEqual(
            response.context_data['status_list'],
            statuses,
            ordered=False,
        )

    def test_create(self):
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
        exist_status = Status.objects.get(id=2)
        response = self.client.post(reverse('statuses:delete',
                                            args=[exist_status.pk]))
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(messages[0].message, _('Status successfully deleted!'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=2)
