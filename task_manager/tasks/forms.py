from django.forms import ModelForm
from task_manager.tasks.models import Tasks
from task_manager.users.models import Users


class TaskForm(ModelForm):

    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def clean_author(self):
        if not self.cleaned_data['author']:
            return Users()
        return self.cleaned_data['author']


class TaskUpdateForm(ModelForm):

    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor', 'labels']
