from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


class CanSelfManageObject(UserPassesTestMixin):
    denied_url = reverse_lazy('users:index')

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return redirect(self.denied_url)


class CanObjectBeDeleted(UserPassesTestMixin):
    denied_url = reverse_lazy('users:index')
    message = _("You cannot delete this user (he/she has a task to execute)")

    def test_func(self):
        return not self.get_object().tasks.exists() and\
            not self.get_object().tasks_to_do.exists()

    def handle_no_permission(self):
        messages.warning(self.request, self.message)
        return redirect(self.denied_url)
