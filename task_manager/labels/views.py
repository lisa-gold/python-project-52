from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import CustomLoginRequiredMixin


class IndexView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'


class LabelCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Create label'),
        'btn_text': _('Create'),
        'btn_class': 'btn-primary'}
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully added!')


class LabelUpdate(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    extra_context = {
        'title': _('Edit label'),
        'btn_text': _('Edit'),
        'btn_class': 'btn-primary'}
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully updated!')


class LabelDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'form.html'
    extra_context = {
        'title': _('Delete label'),
        'btn_text': _('Yes, delete'),
        'btn_class': 'btn-danger'}
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully deleted!')
    redirect_field_name = reverse_lazy('labels:index')

    def dispatch(self, context, **response_kwargs):
        label = super(LabelDelete, self).get_object()
        if label.task_set.all():
            denied_message = _("Label is in use, you cannot delete it!")
            messages.warning(self.request, denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        return super().dispatch(context, **response_kwargs)
