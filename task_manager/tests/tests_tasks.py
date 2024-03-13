from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.tasks.models import Task
from django.urls import reverse
from task_manager.users.models import CustomUser
from django.contrib.messages import get_messages
from task_manager.statuses.models import Status


class TasksTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(first_name='Sara',
                                  last_name='Connor',
                                  username='sara')
        Status.objects.create(name='completed')
        Task.objects.create(name='feed the cat',
                            status=Status.objects.get(name='completed'),
                            author=CustomUser.objects.get(first_name='Sara'))

    def test_index_page(self):
        # without authorization
        self.client.logout()
        response = self.client.get(reverse('tasks:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(messages[0].message,
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

        # logged in
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.all()
        self.assertQuerysetEqual(
            response.context_data['task_list'],
            tasks,
            ordered=False,
        )
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)

    # def test_create(self):
    #     self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
    #     response = self.client.get(reverse('tasks:create'))
    #     self.assertEqual(response.status_code, 200)

    #     new_task = {'name': 'walk the dog',
    #                 'status': Status.objects.get(name='completed'),
    #                 'author': CustomUser.objects.get(first_name='Sara')}
    #     response = self.client.post(reverse('tasks:create'), new_task)
    #     messages = list(get_messages(response.wsgi_request))
    #     created_task = Task.objects.get(name='walk the dog')
    #     self.assertEqual(messages[0].message, 'Задача успешно создана')
    #     self.assertEqual(created_task.name, 'walk the dog')
    #     self.assertRedirects(response, reverse('tasks:index'))
    #     self.assertEqual(created_task.status.name, 'completed')

    def test_update(self):
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        exist_task = Task.objects.get(name='feed the cat')
        response = self.client.get(reverse('tasks:update',
                                           args=[exist_task.pk]))
        self.assertEqual(response.status_code, 200)

        new_task = {'name': 'walk the dog',
                    'status': Status.objects.get(name='completed')}
        response = self.client.post(
            reverse('tasks:update', args=[exist_task.pk]),
            new_task,
        )
        # messages = list(get_messages(response.wsgi_request))

        # self.assertRedirects(response, reverse('tasks:index'))
        # updated_task = Task.objects.get(pk=exist_task.pk)
        # self.assertEqual(updated_task.name, 'walk the dog')
        # self.assertEqual(messages[0].message, 'Задача успешно изменена')

    def test_delete(self):
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        exist_task = Task.objects.get(name='feed the cat')
        response = self.client.post(reverse('tasks:delete',
                                            args=[exist_task.pk]))
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(messages[0].message, 'Задача успешно удалена')
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(name='feed the cat')
