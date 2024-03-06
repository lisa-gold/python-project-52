from django.views.generic import (
                                  ListView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView,
                                  DetailView
                                 )
from task_manager.tasks.models import Tasks
from task_manager.tasks.forms import TaskForm, TaskUpdateForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect


class CustomLoginRequiredMixin(LoginRequiredMixin):
    permission_denied_message = 'To open this page log in!'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR,
                                 self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IndexView(CustomLoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/index.html'
    login_url = reverse_lazy('login')


class TaskDetail(DetailView):
    model = Tasks
    template_name = 'tasks/detail.html'
    login_url = reverse_lazy('login')


class TaskCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Task successfully added!'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class TaskUpdate(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskUpdateForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Task successfully updated!'
    login_url = reverse_lazy('login')


class TaskDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Task successfully deleted!'
    login_url = reverse_lazy('login')
    redirect_field_name = reverse_lazy('tasks:index')

    def render_to_response(self, context, **response_kwargs):
        task = super(TaskDelete, self).get_object()
        if not task.author == self.request.user:
            permission_denied_message = "Only task's author can delete it!"
            messages.warning(self.request, permission_denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        return super().render_to_response(context, **response_kwargs)
