from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.users.models import Users
from django.urls import reverse


class UsersTestCase(TestCase):
    def setUp(self):
        Users.objects.create(first_name='John', last_name='Snow', username='wolf')
        Users.objects.create(first_name='Luke', last_name='Skywalker', username='neo')


    def test_index_page(self):
        response = self.client.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200)

        users = Users.objects.all()
        self.assertQuerysetEqual(
            response.context['users_list'],
            users,
            ordered=False,
        )

    def test_create_page(self):
        response = self.client.get(reverse('users:create'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        Users.objects.create(first_name='Sara', last_name='Conor', username='sara')
        # new_user = {'first_name': 'Sara', 'last_name': 'Connor', 'username': 'sara'}
        # response = self.client.post(reverse('users:create'), new_user)

        # self.assertRedirects(response, reverse('login'))
        created_user = Users.objects.get(first_name='Sara')
        self.assertEqual(created_user.username, 'sara')

    def test_update_page(self):
        exist_user = Users.objects.get(first_name='John')
        response = self.client.get(reverse('users:update', args=[exist_user.pk]))

        self.assertEqual(response.status_code, 200)

    def test_update(self):
        exist_user = Users.objects.get(first_name='John')
        new_user = {'first_name': 'John', 'last_name': 'Stark', 'username': 'wolf'}
        response = self.client.post(
            reverse('users:update', args=[exist_user.pk]),
            new_user,
        )

        self.assertRedirects(response, reverse('users:index'))
        updated_user = Users.objects.get(first_name='John')
        self.assertEqual(updated_user.last_name, 'Stark')

    def test_delete_page(self):
        exist_user = Users.objects.get(first_name='John')
        response = self.client.get(reverse('users:delete', args=[exist_user.pk]))

        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        exist_user = Users.objects.get(first_name='John')
        response = self.client.post(reverse('users:delete', args=[exist_user.pk]))

        self.assertRedirects(response, reverse('users:index'))
        with self.assertRaises(ObjectDoesNotExist):
            Users.objects.get(first_name='John')
