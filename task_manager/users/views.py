from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.users.models import Users
from task_manager.users.forms import UserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _


class IndexView(ListView):
    model = Users
    template_name = 'users/index.html'


class UserCreate(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('Successfully registered!')


class UserUpdate(SuccessMessageMixin, UpdateView):
    model = Users
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')
    success_message = _('Successfully updated!')
    redirect_field_name = reverse_lazy('users:index')

    def render_to_response(self, context, **response_kwargs):
        user_to_update = super(UserUpdate, self).get_object()
        if not user_to_update.id == self.request.user.id:
            permission_denied_message = _("You cannot edit other users!")
            messages.warning(self.request, permission_denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        return super().render_to_response(context, **response_kwargs)


class UserDelete(SuccessMessageMixin, DeleteView):
    model = Users
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
    success_message = _('Successfully deleted!')
    redirect_field_name = reverse_lazy('users:index')

    def render_to_response(self, context, **response_kwargs):
        user_to_delete = super(UserDelete, self).get_object()
        if not user_to_delete.id == self.request.user.id:
            permission_denied_message = _("You cannot delete other users!")
            messages.warning(self.request, permission_denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        if user_to_delete.tasks.all() or user_to_delete.tasks_to_do.all():
            denied_message = _("You cannot delete this user because\
                              he/she has a task to execute!")
            messages.warning(self.request, denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        return super().render_to_response(context, **response_kwargs)


class UserUpdatePassward(UpdateView):
    model = Users
    template_name = 'users/passward.html'
