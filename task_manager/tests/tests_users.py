from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.users.models import CustomUser
from django.urls import reverse


class UsersTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(first_name='John',
                                  last_name='Snow',
                                  username='wolf')
        CustomUser.objects.create(first_name='Luke',
                                  last_name='Skywalker',
                                  username='neo')

    def test_index_page(self):
        response = self.client.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200)

        users = CustomUser.objects.all()
        self.assertQuerysetEqual(
            response.context['customuser_list'],
            users,
            ordered=False,
        )

    def test_create_page(self):
        response = self.client.get(reverse('users:create'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        CustomUser.objects.create(first_name='Sara',
                                  last_name='Conor',
                                  username='sara')

        created_user = CustomUser.objects.get(first_name='Sara')
        self.assertEqual(created_user.username, 'sara')

    def test_update_page(self):
        exist_user = CustomUser.objects.get(first_name='John')
        response = self.client.get(reverse('users:update',
                                   args=[exist_user.pk]))

        self.assertEqual(response.status_code, 302)

    def test_update(self):
        exist_user = CustomUser.objects.get(first_name='John')
        new_user = {'first_name': 'John',
                    'last_name': 'Stark',
                    'username': 'wolf'}
        response = self.client.post(
            reverse('users:update', args=[exist_user.pk]),
            new_user,
        )

        # not logged in
        self.assertRedirects(response, reverse('users:index'))
        not_updated_user = CustomUser.objects.get(first_name='John')
        self.assertEqual(not_updated_user.last_name, 'Snow')

        # logged in
        self.client.force_login(user=exist_user)
        response = self.client.post(
            reverse('users:update', args=[exist_user.pk]),
            new_user,
        )
        # updated_user = CustomUser.objects.get(first_name='John')
        # self.assertEqual(updated_user.last_name, 'Stark')

    def test_delete_page(self):
        exist_user = CustomUser.objects.get(first_name='John')
        response = self.client.get(reverse('users:delete',
                                           args=[exist_user.pk]))

        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        exist_user = CustomUser.objects.get(first_name='John')
        response = self.client.post(reverse('users:delete',
                                            args=[exist_user.pk]))

        self.assertRedirects(response, reverse('users:index'))
        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(first_name='John')
