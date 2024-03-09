from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm, StatusUpdateForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    permission_denied_message = _('To open this page log in!')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING,
                                 self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IndexView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    login_url = reverse_lazy('login')


class StatusCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully added!')


class StatusUpdate(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusUpdateForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully updated!')


class StatusDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully deleted!')
    redirect_field_name = reverse_lazy('statuses:index')

    def render_to_response(self, context, **response_kwargs):
        status = super(StatusDelete, self).get_object()
        if status.task_set.all():
            denied_message = _("Status is in use, you cannot delete it!")
            messages.warning(self.request, denied_message)
            return HttpResponseRedirect(self.redirect_field_name)
        return super().render_to_response(context, **response_kwargs)
