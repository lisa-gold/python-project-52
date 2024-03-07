import django_filters
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels


class TaskFilter(django_filters.FilterSet):
    label = django_filters.ModelChoiceFilter(
                                             queryset=Labels.objects.all(),
                                             field_name='labels')

    class Meta:
        model = Tasks
        fields = ['status', 'executor']
    