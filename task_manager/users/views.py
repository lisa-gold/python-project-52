from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.users.models import CustomUser
from task_manager.users.forms import UserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import UserPassesTestMixin


class IndexView(ListView):
    model = CustomUser
    template_name = 'users/index.html'


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

    def test_func_tasks(self):
        return self.get_object().tasks.all() or\
            self.get_object().tasks_to_do.all()

    def handle_no_permission_tasks(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.warning(self.request, self.denied_message)
            return redirect(self.redirect_field_name)
        return super().handle_no_permission()


class UserCreate(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Registration'),
        'btn_text': _('Sign up'),
        'btn_class': 'btn-primary'}
    success_url = reverse_lazy('login')
    success_message = _('Successfully registered!')


class UserUpdate(SuccessMessageMixin, UpdateView, OwnerPermission):
    model = CustomUser
    form_class = UserForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Edit user'),
        'btn_text': _('Update'),
        'btn_class': 'btn-primary'}
    success_message = _('Successfully updated!')
    success_url = reverse_lazy('users:index')
    permission_denied_message = _("You cannot edit other users!")

    def dispatch(self, context, **response_kwargs):
        if not super().test_func():
            return super().handle_no_permission()
        return super().dispatch(context, **response_kwargs)


class UserDelete(SuccessMessageMixin, DeleteView, OwnerPermission, UserHasTask):
    model = CustomUser
    template_name = 'form.html'
    extra_context = {
        'title': _('Delete user'),
        'btn_text': _('Yes, delete'),
        'btn_class': 'btn-danger'}
    success_message = _('Successfully deleted!')
    success_url = reverse_lazy('users:index')
    permission_denied_message = _("You cannot delete other users!")

    def dispatch(self, context, **response_kwargs):
        if not super().test_func():
            return super().handle_no_permission()
        if super().test_func_tasks():
            return super().handle_no_permission_tasks()
        return super().dispatch(context, **response_kwargs)
