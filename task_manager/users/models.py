from django.contrib.auth.models import User
from django.urls import reverse


class CustomUser(User):

    def get_absolute_url(self):
        return reverse('users:index')
