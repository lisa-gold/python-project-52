from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.statuses.models import Statuses
from task_manager.statuses.forms import StatusForm, StatusUpdateForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CustomLoginRequiredMixin(LoginRequiredMixin):
    permission_denied_message = 'To open this page log in!'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING,
                                 self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IndexView(CustomLoginRequiredMixin, ListView):
    model = Statuses
    template_name = 'statuses/index.html'
    login_url = reverse_lazy('login')


class StatusCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Status successfully added!'
    login_url = reverse_lazy('login')


class StatusUpdate(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Statuses
    form_class = StatusUpdateForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Status successfully updated!'
    login_url = reverse_lazy('login')


class StatusDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Statuses
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Status successfully deleted!'
    login_url = reverse_lazy('login')
