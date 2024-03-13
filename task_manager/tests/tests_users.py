from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.users.models import CustomUser
from django.urls import reverse
from json import load
from task_manager.settings import BASE_DIR
from django.contrib.messages import get_messages


FIXTURES = f'{BASE_DIR}/task_manager/tests/fixtures'


def get_content(filename):
    with open(f'{FIXTURES}/{filename}') as file:
        return load(file)


class UsersTestCase(TestCase):
    fixtures = ['users_db.json']

    def setUp(self):
        CustomUser.objects.create(first_name='John',
                                  last_name='Snow',
                                  username='wolf')
        CustomUser.objects.create(first_name='Sara',
                                  last_name='Connor',
                                  username='sara')

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
        new_user = get_content('users_data.json').get('user_new')
        response = self.client.post(reverse('users:create'),
                                    new_user)
        created_user = CustomUser.objects.get(first_name='Luke')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(created_user.username, 'neo')
        self.assertEqual(messages[0].message,
                         'Пользователь успешно зарегистрирован')

    def test_update(self):
        exist_user = CustomUser.objects.get(first_name='John')
        updated_user = get_content('users_data.json').get('user_updated')

        # try to change another user
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        response = self.client.get(reverse('users:update',
                                   args=[exist_user.pk]),
                                   updated_user)

        not_updated_user = CustomUser.objects.get(first_name='John')
        messages_denied = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(not_updated_user.last_name, 'Snow')
        self.assertEqual(messages_denied[0].message,
                         'У вас нет прав для изменения другого пользователя.')

        # logged in
        self.client.force_login(user=exist_user)
        response = self.client.post(reverse('users:update',
                                            args=[exist_user.pk]),
                                    updated_user)
        updated_user_added = CustomUser.objects.get(first_name='John')
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_user_added.last_name, 'Stark')
        self.assertEqual(messages[0].message, 'Пользователь успешно изменен')
        self.assertRedirects(response, reverse('users:index'))

    def test_delete(self):
        exist_user = CustomUser.objects.get(first_name='John')

        # try to change another user
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        response = self.client.get(reverse('users:delete',
                                           args=[exist_user.pk]))
        messages_denied = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(exist_user.first_name, 'John')
        self.assertEqual(messages_denied[0].message,
                         'У вас нет прав для изменения другого пользователя.')

        # logged in
        self.client.force_login(user=exist_user)
        response = self.client.post(reverse('users:delete',
                                            args=[exist_user.pk]))
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(messages[0].message, 'Пользователь успешно удален')
        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(first_name='John')
