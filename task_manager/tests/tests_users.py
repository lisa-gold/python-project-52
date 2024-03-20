from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.users.models import CustomUser
from django.urls import reverse
from . import get_content
from django.utils.translation import gettext_lazy as _


class UsersTestCase(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.dump_data = get_content('data.json')

    def test_index_page(self):
        response = self.client.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200)

        users = CustomUser.objects.all()
        count = users.count()
        self.assertEqual(count, 2)
        self.assertQuerysetEqual(
            response.context['customuser_list'],
            users,
            ordered=False,
        )

    def test_create(self):
        response = self.client.get(reverse('users:create'))
        self.assertEqual(response.status_code, 200)

        new_user = self.dump_data.get('users').get('new')
        response = self.client.post(reverse('users:create'),
                                    new_user,
                                    follow=True)
        created_user = CustomUser.objects.get(id=new_user.get('pk'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(created_user.username, new_user.get('username'))
        self.assertContains(response, _('Successfully registered!'))

    def test_update(self):
        exist_user = CustomUser.objects.get(id=1)
        updated_user = self.dump_data.get('users').get('updated')

        # try to change another user
        self.client.force_login(user=CustomUser.objects.get(id=2))
        response = self.client.get(reverse('users:update',
                                   args=[exist_user.pk]),
                                   updated_user,
                                   follow=True)

        not_updated_user = CustomUser.objects.get(id=exist_user.pk)

        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(not_updated_user.last_name, exist_user.last_name)
        self.assertContains(response, _('You cannot edit other users!'))

        # logged in
        self.client.force_login(user=exist_user)
        response = self.client.post(reverse('users:update',
                                            args=[exist_user.pk]),
                                    updated_user,
                                    follow=True)
        updated_user_added = CustomUser.objects.get(id=exist_user.pk)

        self.assertEqual(updated_user_added.last_name, 'Stark')
        self.assertContains(response, _('Successfully updated!'))
        self.assertRedirects(response, reverse('users:index'))

    def test_delete(self):
        exist_user = CustomUser.objects.get(id=1)

        # try to change another user
        self.client.force_login(user=CustomUser.objects.get(id=2))
        response = self.client.get(reverse('users:delete',
                                           args=[exist_user.pk]),
                                   follow=True)

        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(exist_user.first_name, 'John')
        self.assertContains(response, _("You cannot delete other users!"))

        # logged in
        self.client.force_login(user=exist_user)
        response = self.client.post(reverse('users:delete',
                                            args=[exist_user.pk]),
                                    follow=True)

        self.assertRedirects(response, reverse('users:index'))
        self.assertContains(response, _('Successfully deleted!'))
        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(id=1)
