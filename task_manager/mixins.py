from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    permission_denied_message = _('To open this page log in!')
    redirect_field_name = ''
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.warning(self.request,
                             CustomLoginRequiredMixin.permission_denied_message,
                             extra_tags='danger')
        return super().handle_no_permission()
