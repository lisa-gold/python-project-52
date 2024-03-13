from django.views.generic import (CreateView,
                                  DeleteView,
                                  UpdateView,
                                  DetailView)
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filter import TaskFilter
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import CustomLoginRequiredMixin


class IndexView(CustomLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter


class TaskDetail(DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class TaskCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Create task'),
        'btn_text': _('Create'),
        'btn_class': 'btn-primary'}
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully added!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdate(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Edit task'),
        'btn_text': _('Edit'),
        'btn_class': 'btn-primary'}
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully updated!')


class TaskDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'form.html'
    extra_context = {
        'title': _('Delete task'),
        'btn_text': _('Yes, delete'),
        'btn_class': 'btn-danger'}
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully deleted!')
    redirect_field_name = reverse_lazy('tasks:index')

    def dispatch(self, context, **response_kwargs):
        task = super(TaskDelete, self).get_object()
        if not task.author == self.request.user:
            permission_denied_message = _("Only task's author can delete it!")
            messages.warning(self.request, permission_denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        return super().dispatch(context, **response_kwargs)
