from django.forms import ModelForm
from task_manager.statuses.models import Status


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']


class StatusUpdateForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']
