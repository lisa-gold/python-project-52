from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.statuses.models import Statuses
from django.urls import reverse
from django.contrib.auth.models import User


class StatusesTestCase(TestCase):
    def setUp(self):
        Statuses.objects.create(name='in progress')
        Statuses.objects.create(name='completed')
        self.client.login(username='fred', password='secret')

    def test_index_page(self):
        response = self.client.get(reverse('statuses:index'))
        self.assertEqual(response.status_code, 302)

    def test_create_page(self):
        self.client.login(username='fred', password='secret')
        response = self.client.get(reverse('statuses:create'))
        self.assertEqual(response.status_code, 302)

    def test_create(self):
        self.client.login(username='fred', password='secret')
        Statuses.objects.create(name='25%')
        created_status = Statuses.objects.get(name='25%')
        self.assertEqual(created_status.name, '25%')

    def test_update_page(self):
        self.client.login(username='fred', password='secret')
        exist_status = Statuses.objects.get(name='completed')
        response = self.client.get(reverse('statuses:update',
                                           args=[exist_status.pk]))
        self.assertEqual(response.status_code, 302)

    def test_update(self):
        user = User.objects.create_user("john")
        self.client.force_login(user=user)
        exist_status = Statuses.objects.get(name='completed')
        new_status = {'name': '50%'}
        response = self.client.post(
            reverse('statuses:update', args=[exist_status.pk]),
            new_status,
        )

        self.assertRedirects(response, reverse('statuses:index'))
        updated_status = Statuses.objects.get(pk=exist_status.pk)
        self.assertEqual(updated_status.name, '50%')

    def test_delete_page(self):
        self.client.login(username='fred', password='secret')
        exist_status = Statuses.objects.get(name='completed')
        response = self.client.get(reverse('statuses:delete',
                                           args=[exist_status.pk]))

        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        user = User.objects.create_user("john")
        self.client.force_login(user=user)
        exist_status = Statuses.objects.get(name='completed')
        response = self.client.post(reverse('statuses:delete',
                                            args=[exist_status.pk]))

        self.assertRedirects(response, reverse('statuses:index'))
        with self.assertRaises(ObjectDoesNotExist):
            Statuses.objects.get(name='completed')
