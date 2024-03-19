from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_message = _('To open this page log in!')
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.warning(self.request,
                             self.login_message,
                             extra_tags='danger')
            return redirect(self.login_url)
        return super().handle_no_permission()
