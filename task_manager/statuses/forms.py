from django.forms import ModelForm
from task_manager.statuses.models import Statuses


class StatusForm(ModelForm):

    class Meta:
        model = Statuses
        fields = ['name']


class StatusUpdateForm(ModelForm):

    class Meta:
        model = Statuses
        fields = ['name']
