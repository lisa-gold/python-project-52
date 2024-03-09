import django_filters
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django import forms


class TaskFilter(django_filters.FilterSet):

    def filter_own_tasks(self, queryset, arg, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    label = django_filters.ModelChoiceFilter(
                                             queryset=Label.objects.all(),
                                             field_name='labels')
    is_author = django_filters.BooleanFilter(field_name='author',
                                             widget=forms.CheckboxInput,
                                             method='filter_own_tasks',
                                             label='Only my tasks')

    class Meta:
        model = Task
        fields = ['status', 'executor']
