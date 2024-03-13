from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.statuses.models import Status
from django.urls import reverse
from task_manager.users.models import CustomUser
from django.contrib.messages import get_messages


class StatusesTestCase(TestCase):
    def setUp(self):
        Status.objects.create(name='completed')
        CustomUser.objects.create(first_name='Sara',
                                  last_name='Connor',
                                  username='sara')

    def test_index_page(self):
        # without authorization
        self.client.logout()
        response = self.client.get(reverse('statuses:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(messages[0].message,
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

        # logged in
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        response = self.client.get(reverse('statuses:index'))
        self.assertEqual(response.status_code, 200)

        statuses = Status.objects.all()
        self.assertQuerysetEqual(
            response.context_data['status_list'],
            statuses,
            ordered=False,
        )

    def test_create(self):
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        response = self.client.get(reverse('statuses:create'))
        self.assertEqual(response.status_code, 200)

        new_status = {'name': '25%'}
        response = self.client.post(reverse('statuses:create'), new_status)
        created_status = Status.objects.get(name='25%')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(created_status.name, '25%')
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(messages[0].message, 'Статус успешно создан')

    def test_update(self):
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        exist_status = Status.objects.get(name='completed')
        response = self.client.get(reverse('statuses:update',
                                           args=[exist_status.pk]))
        self.assertEqual(response.status_code, 200)

        new_status = {'name': '50%'}
        response = self.client.post(
            reverse('statuses:update', args=[exist_status.pk]),
            new_status,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('statuses:index'))
        updated_status = Status.objects.get(pk=exist_status.pk)
        self.assertEqual(updated_status.name, '50%')
        self.assertEqual(messages[0].message, 'Статус успешно изменен')

    def test_delete(self):
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        exist_status = Status.objects.get(name='completed')
        response = self.client.post(reverse('statuses:delete',
                                            args=[exist_status.pk]))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(messages[0].message, 'Статус успешно удален')
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(name='completed')
