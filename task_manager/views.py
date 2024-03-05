from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


MESSAGE_TAGS = {
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
        }


class IndexView(TemplateView):
    template_name = 'index.html'


class Login(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    success_message = 'Successfully logged in!'


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Successfully logged out!')
    return redirect('index')
