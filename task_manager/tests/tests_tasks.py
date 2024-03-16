from task_manager.tests.test_auth import AuthTestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.tasks.models import Task
from django.urls import reverse
from task_manager.users.models import CustomUser
from django.contrib.messages import get_messages
from task_manager.tests.parser import get_content
from django.utils.translation import gettext_lazy as _


class TasksTestCase(AuthTestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.dump_data = get_content('data.json')

    def test_index_page(self):
        # without authorization
        self.client.logout()
        response = self.client.get(reverse('tasks:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(messages[0].message,
                         _('To open this page log in!'))

        # logged in
        self.client.force_login(user=CustomUser.objects.get(id=1))
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.all()
        count = tasks.count()
        self.assertEqual(count, 1)
        self.assertQuerysetEqual(
            response.context_data['task_list'],
            tasks,
            ordered=False,
        )
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        self.client.force_login(user=CustomUser.objects.get(id=1))
        response_get = self.client.get(reverse('tasks:create'))
        self.assertEqual(response_get.status_code, 200)

        new_task = self.dump_data.get('tasks').get('new')
        response = self.client.post(reverse('tasks:create'), new_task)
        messages = list(get_messages(response.wsgi_request))
        created_task = Task.objects.get(id=new_task.get('pk'))
        count = Task.objects.all().count()
        self.assertEqual(count, 2)
        self.assertEqual(messages[0].message, _('Task successfully added!'))
        self.assertEqual(created_task.name, new_task.get('name'))
        self.assertRedirects(response, reverse('tasks:index'))

    def test_update(self):
        self.client.force_login(user=CustomUser.objects.get(id=1))
        exist_task = Task.objects.get(id=1)
        response = self.client.get(reverse('tasks:update',
                                           args=[exist_task.pk]))
        self.assertEqual(response.status_code, 200)

        new_task = self.dump_data.get('tasks').get('updated')
        response = self.client.post(
            reverse('tasks:update', args=[exist_task.pk]),
            new_task,
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('tasks:index'))
        updated_task = Task.objects.get(pk=exist_task.pk)
        self.assertEqual(updated_task.name, new_task.get('name'))
        self.assertEqual(messages[0].message, _('Задача успешно изменена'))

    def test_delete(self):
        self.client.force_login(user=CustomUser.objects.get(id=2))
        exist_task = Task.objects.get(id=1)
        response = self.client.post(reverse('tasks:delete',
                                            args=[exist_task.pk]))
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(messages[0].message, _('Задача успешно удалена'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=1)
