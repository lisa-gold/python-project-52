from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from task_manager.labels.models import Label
from django.urls import reverse
from task_manager.users.models import CustomUser
from django.contrib.messages import get_messages


class LabelsTestCase(TestCase):
    def setUp(self):
        Label.objects.create(name='easy')
        CustomUser.objects.create(first_name='Sara',
                                  last_name='Connor',
                                  username='sara')

    def test_index_page(self):
        # without authorization
        self.client.logout()
        response = self.client.get(reverse('labels:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(messages[0].message,
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

        # logged in
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        response = self.client.get(reverse('labels:index'))
        self.assertEqual(response.status_code, 200)

        labels = Label.objects.all()
        self.assertQuerysetEqual(
            response.context_data['label_list'],
            labels,
            ordered=False,
        )

    def test_create(self):
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        response = self.client.get(reverse('labels:create'))
        self.assertEqual(response.status_code, 200)
        new_label = {'name': 'urgent'}
        response = self.client.post(reverse('labels:create'), new_label)
        messages = list(get_messages(response.wsgi_request))
        created_label = Label.objects.get(name='urgent')
        self.assertEqual(created_label.name, 'urgent')
        self.assertRedirects(response, reverse('labels:index'))
        self.assertEqual(messages[0].message, 'Метка успешно создана')

    def test_update(self):
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        exist_label = Label.objects.get(name='easy')
        response = self.client.get(reverse('labels:update',
                                           args=[exist_label.pk]))
        self.assertEqual(response.status_code, 200)

        new_label = {'name': 'difficult'}
        response = self.client.post(
            reverse('labels:update', args=[exist_label.pk]),
            new_label,
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('labels:index'))
        updated_label = Label.objects.get(pk=exist_label.pk)
        self.assertEqual(updated_label.name, 'difficult')
        self.assertEqual(messages[0].message, 'Метка успешно изменена')

    def test_delete(self):
        self.client.force_login(user=CustomUser.objects.get(first_name='Sara'))
        exist_label = Label.objects.get(name='easy')

        response = self.client.post(reverse('labels:delete',
                                            args=[exist_label.pk]))

        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, reverse('labels:index'))
        self.assertEqual(messages[0].message, 'Метка успешно удалена')
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(name='easy')
