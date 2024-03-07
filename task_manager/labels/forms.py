from django.forms import ModelForm
from task_manager.labels.models import Labels


class LabelForm(ModelForm):

    class Meta:
        model = Labels
        fields = ['name']


class LabelUpdateForm(ModelForm):

    class Meta:
        model = Labels
        fields = ['name']
