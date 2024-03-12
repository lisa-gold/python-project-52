from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.users.models import CustomUser
from task_manager.users.forms import UserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _


class IndexView(ListView):
    model = CustomUser
    template_name = 'users/index.html'


class Permission:
    redirect_field_name = reverse_lazy('users:index')
    permission_denied_message = ''
    denied_message = ''

    def check_permission(self, context, user_to_modify, **response_kwargs):
        if not user_to_modify.id == self.request.user.id:
            messages.warning(self.request, self.permission_denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        if user_to_modify.tasks.all() or user_to_modify.tasks_to_do.all():
            messages.warning(self.request, self.denied_message)
            return HttpResponseRedirect(self.redirect_field_name)


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


class UserUpdate(SuccessMessageMixin, UpdateView, Permission):
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

    def render_to_response(self, context, **response_kwargs):
        user_to_update = super(UserUpdate, self).get_object()
        is_permission = super().check_permission(context,
                                                 user_to_update,
                                                 **response_kwargs)
        if is_permission:
            return is_permission
        return super().render_to_response(context, **response_kwargs)


class UserDelete(SuccessMessageMixin, DeleteView, Permission):
    model = CustomUser
    template_name = 'form.html'
    extra_context = {
        'title': _('Delete user'),
        'btn_text': _('Yes, delete'),
        'btn_class': 'btn-danger'}
    success_message = _('Successfully deleted!')
    success_url = reverse_lazy('users:index')
    permission_denied_message = _("You cannot delete other users!")
    denied_message = _("You cannot delete this user because\
                       he/she has a task to execute!")

    def render_to_response(self, context, **response_kwargs):
        user_to_delete = super(UserDelete, self).get_object()
        is_permission = super().check_permission(context,
                                                 user_to_delete,
                                                 **response_kwargs)
        if is_permission:
            return is_permission
        return super().render_to_response(context, **response_kwargs)
