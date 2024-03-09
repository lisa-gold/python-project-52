from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.tasks.models import Task
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class TasksTestCase(TestCase):
    def setUp(self):
        Status.objects.create(name='completed')
        Task.objects.create(name='feed the cat',
                            status=Status.objects.get(name='completed'))
        self.client.login(username='fred', password='secret')

    def test_index_page(self):
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 302)

    def test_create_page(self):
        self.client.login(username='fred', password='secret')
        response = self.client.get(reverse('tasks:create'))
        self.assertEqual(response.status_code, 302)

    def test_create(self):
        self.client.login(username='fred', password='secret')
        Task.objects.create(name='walk the dog',
                            status=Status.objects.get(name='completed'))
        created_task = Task.objects.get(name='walk the dog')
        self.assertEqual(created_task.status.name, 'completed')

    def test_update_page(self):
        self.client.login(username='fred', password='secret')
        exist_task = Task.objects.get(name='feed the cat')
        response = self.client.get(reverse('tasks:update',
                                           args=[exist_task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_page(self):
        self.client.login(username='fred', password='secret')
        exist_task = Task.objects.get(name='feed the cat')
        response = self.client.get(reverse('tasks:delete',
                                           args=[exist_task.pk]))

        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        user = User.objects.create_user("john")
        self.client.force_login(user=user)
        exist_task = Task.objects.get(name='feed the cat')
        response = self.client.post(reverse('tasks:delete',
                                            args=[exist_task.pk]))

        self.assertRedirects(response, reverse('tasks:index'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(name='feed the cat')
