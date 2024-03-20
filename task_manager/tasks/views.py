from django.views.generic import (CreateView,
                                  DeleteView,
                                  UpdateView,
                                  DetailView)
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filter import TaskFilter
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.tasks.mixins import TaskAuthorMixin


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


class TaskDelete(CustomLoginRequiredMixin, SuccessMessageMixin,
                 TaskAuthorMixin, DeleteView):
    model = Task
    template_name = 'form.html'
    extra_context = {
        'title': _('Delete task'),
        'btn_text': _('Yes, delete'),
        'btn_class': 'btn-danger'}
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully deleted!')
    fail_url = reverse_lazy('tasks:index')
