from django.contrib.auth.models import User
from django.urls import reverse


class Users(User):

    def get_absolute_url(self):
        return reverse('users:index')
