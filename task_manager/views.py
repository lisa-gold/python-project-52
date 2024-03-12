from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):
    template_name = 'index.html'


class Login(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    success_message = _('Successfully logged in!')


class Logout(SuccessMessageMixin, LogoutView):
    success_url = reverse_lazy('index')
    success_message = _('Successfully logged out!')

    def post(self, request, *args, **kwargs):
        messages.add_message(request,
                             messages.INFO,
                             _('Successfully logged out!'))
        return super().post(request, *args, **kwargs)
