from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerPermission(UserPassesTestMixin):
    redirect_field_name = reverse_lazy('users:index')
    permission_denied_message = ''

    def test_func(self):
        return self.get_object().id == self.request.user.id

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.warning(self.request, self.permission_denied_message)
            return redirect(self.redirect_field_name)
        return super().handle_no_permission()


class UserHasTask(UserPassesTestMixin):
    redirect_field_name = reverse_lazy('users:index')
    denied_message = _("You cannot delete this user because\
                       he/she has a task to execute!")

    def test_func(self):
        return self.get_object().tasks.all() or\
            self.get_object().tasks_to_do.all()

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.warning(self.request, self.denied_message)
            return redirect(self.redirect_field_name)
        return super().handle_no_permission()
