from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.users.models import Users
from task_manager.users.forms import UserForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


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


class UserDelete(SuccessMessageMixin, DeleteView):
    model = Users
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
    success_message = 'Successfully deleted!'


class UserUpdatePassward(UpdateView):
    model = Users
    template_name = 'users/passward.html'
