from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.users.models import Users
from task_manager.users.forms import UserForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect


class IndexView(ListView):
    model = Users
    template_name = 'users/index.html'


class UserCreate(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Successfully registered!'


class UserUpdate(SuccessMessageMixin, UpdateView):
    model = Users
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')
    success_message = 'Successfully updated!'
    redirect_field_name = reverse_lazy('users:index')

    def render_to_response(self, context, **response_kwargs):
        user_to_update = super(UserUpdate, self).get_object()
        if not user_to_update == self.request.user:
            permission_denied_message = "You cannot edit other users!"
            messages.warning(self.request, permission_denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        return super().render_to_response(context, **response_kwargs)


class UserDelete(SuccessMessageMixin, DeleteView):
    model = Users
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
    success_message = 'Successfully deleted!'
    redirect_field_name = reverse_lazy('users:index')

    def render_to_response(self, context, **response_kwargs):
        user_to_delete = super(UserDelete, self).get_object()
        if not user_to_delete == self.request.user:
            permission_denied_message = "You cannot delete other users!"
            messages.warning(self.request, permission_denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        return super().render_to_response(context, **response_kwargs)


class UserUpdatePassward(UpdateView):
    model = Users
    template_name = 'users/passward.html'
