from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import CustomLoginRequiredMixin


class IndexView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'


class StatusCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Create status'),
        'btn_text': _('Create'),
        'btn_class': 'btn-primary'}
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully added!')


class StatusUpdate(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Edit status'),
        'btn_text': _('Edit'),
        'btn_class': 'btn-primary'}
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully updated!')


class StatusDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'form.html'
    extra_context = {
        'title': _('Delete status'),
        'btn_text': _('Yes, delete'),
        'btn_class': 'btn-danger'}
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully deleted!')
    redirect_field_name = reverse_lazy('statuses:index')

    def dispatch(self, context, **response_kwargs):
        status = super(StatusDelete, self).get_object()
        if status.task_set.all():
            denied_message = _("Status is in use, you cannot delete it!")
            messages.warning(self.request, denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        return super().dispatch(context, **response_kwargs)
