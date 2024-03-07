from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.labels.models import Labels
from django.urls import reverse
from django.contrib.auth.models import User


class LabelsTestCase(TestCase):
    def setUp(self):
        Labels.objects.create(name='easy')
        self.client.login(username='fred', password='secret')

    def test_index_page(self):
        response = self.client.get(reverse('labels:index'))
        self.assertEqual(response.status_code, 302)

    def test_create_page(self):
        self.client.login(username='fred', password='secret')
        response = self.client.get(reverse('labels:create'))
        self.assertEqual(response.status_code, 302)

    def test_create(self):
        self.client.login(username='fred', password='secret')
        Labels.objects.create(name='urgent')
        created_label = Labels.objects.get(name='urgent')
        self.assertEqual(created_label.name, 'urgent')

    def test_update_page(self):
        self.client.login(username='fred', password='secret')
        exist_label = Labels.objects.get(name='easy')
        response = self.client.get(reverse('labels:update',
                                           args=[exist_label.pk]))
        self.assertEqual(response.status_code, 302)

    def test_update(self):
        user = User.objects.create_user("john")
        self.client.force_login(user=user)
        exist_label = Labels.objects.get(name='easy')
        new_label = {'name': 'difficult'}
        response = self.client.post(
            reverse('labels:update', args=[exist_label.pk]),
            new_label,
        )

        self.assertRedirects(response, reverse('labels:index'))
        updated_label = Labels.objects.get(pk=exist_label.pk)
        self.assertEqual(updated_label.name, 'difficult')

    def test_delete_page(self):
        self.client.login(username='fred', password='secret')
        exist_label = Labels.objects.get(name='easy')
        response = self.client.get(reverse('labels:delete',
                                           args=[exist_label.pk]))

        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        user = User.objects.create_user("john")
        self.client.force_login(user=user)
        exist_label = Labels.objects.get(name='easy')
        response = self.client.post(reverse('labels:delete',
                                            args=[exist_label.pk]))

        self.assertRedirects(response, reverse('labels:index'))
        with self.assertRaises(ObjectDoesNotExist):
            Labels.objects.get(name='easy')
