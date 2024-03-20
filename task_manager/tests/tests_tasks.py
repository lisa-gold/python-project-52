from task_manager.tests.test_auth import AuthTestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.tasks.models import Task
from django.urls import reverse
from task_manager.users.models import CustomUser
from . import get_content
from django.utils.translation import gettext_lazy as _


class TasksTestCase(AuthTestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.dump_data = get_content('data.json')
        self.client.force_login(user=CustomUser.objects.get(id=1))

    def test_index_page(self):
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
        response_get = self.client.get(reverse('tasks:create'))
        self.assertEqual(response_get.status_code, 200)

        new_task = self.dump_data.get('tasks').get('new')
        response = self.client.post(reverse('tasks:create'),
                                    new_task,
                                    follow=True)
        created_task = Task.objects.get(id=new_task.get('pk'))
        count = Task.objects.all().count()
        self.assertEqual(count, 2)
        self.assertContains(response, _('Task successfully added!'))
        self.assertEqual(created_task.name, new_task.get('name'))
        self.assertRedirects(response, reverse('tasks:index'))

    def test_update(self):
        exist_task = Task.objects.get(id=1)
        response = self.client.get(reverse('tasks:update',
                                           args=[exist_task.pk]))
        self.assertEqual(response.status_code, 200)

        new_task = self.dump_data.get('tasks').get('updated')
        response = self.client.post(
            reverse('tasks:update', args=[exist_task.pk]),
            new_task,
            follow=True
        )

        self.assertRedirects(response, reverse('tasks:index'))
        updated_task = Task.objects.get(pk=exist_task.pk)
        self.assertEqual(updated_task.name, new_task.get('name'))
        self.assertContains(response, _('Task successfully updated!'))

    def test_delete(self):
        self.client.force_login(user=CustomUser.objects.get(id=2))
        exist_task = Task.objects.get(id=1)
        response = self.client.post(reverse('tasks:delete',
                                            args=[exist_task.pk]),
                                    follow=True)

        self.assertRedirects(response, reverse('tasks:index'))
        self.assertContains(response, _('Task successfully deleted!'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=1)
