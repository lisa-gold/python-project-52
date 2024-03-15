from django.core.exceptions import ObjectDoesNotExist
from task_manager.labels.models import Label
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


class LabelsTestCase(AuthTestCase):
    page = 'labels'

    def setUp(self):
        self.dump_data = get_content('data.json')
        user = self.dump_data.get('users').get('existing1')
        label = self.dump_data.get('labels').get('existing')
        CustomUser.objects.create(**user)
        Label.objects.create(**label)

    def test_index_page(self):
        # logged in
        self.client.force_login(user=CustomUser.objects.get(id=1))
        response = self.client.get(reverse('labels:index'))
        self.assertEqual(response.status_code, 200)

        labels = Label.objects.all()
        count = labels.count()
        self.assertEqual(count, 1)
        self.assertQuerysetEqual(
            response.context_data['label_list'],
            labels,
            ordered=False,
        )

    def test_create(self):
        self.client.force_login(user=CustomUser.objects.get(id=1))
        response = self.client.get(reverse('labels:create'))
        self.assertEqual(response.status_code, 200)
        new_label = self.dump_data.get('labels').get('new')
        response = self.client.post(reverse('labels:create'), new_label)
        messages = list(get_messages(response.wsgi_request))
        created_label = Label.objects.get(id=new_label.get('pk'))
        self.assertEqual(created_label.name, new_label.get('name'))
        self.assertRedirects(response, reverse('labels:index'))
        self.assertEqual(messages[0].message, _('Label successfully added!'))

    def test_update(self):
        self.client.force_login(user=CustomUser.objects.get(id=1))
        exist_label = Label.objects.get(id=1)
        response = self.client.get(reverse('labels:update',
                                           args=[exist_label.pk]))
        self.assertEqual(response.status_code, 200)

        new_label = self.dump_data.get('labels').get('updated')
        response = self.client.post(
            reverse('labels:update', args=[exist_label.pk]),
            new_label,
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('labels:index'))
        updated_label = Label.objects.get(pk=exist_label.pk)
        self.assertEqual(updated_label.name, new_label.get('name'))
        self.assertEqual(messages[0].message, _('Label successfully updated!'))

    def test_delete(self):
        self.client.force_login(user=CustomUser.objects.get(id=1))
        exist_label = Label.objects.get(id=1)

        response = self.client.post(reverse('labels:delete',
                                            args=[exist_label.pk]))

        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('labels:index'))
        self.assertEqual(messages[0].message, _('Label successfully deleted!'))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=1)
