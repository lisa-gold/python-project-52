from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django import forms


class Users(User):

    def get_absolute_url(self):
        return reverse('users:index')
