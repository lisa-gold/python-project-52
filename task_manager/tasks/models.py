from django.db import models
from task_manager.users.models import CustomUser
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    author = models.ForeignKey(User,
                               on_delete=models.PROTECT,
                               related_name='tasks',
                               blank=True,
                               null=True,
                               verbose_name=_('Author'))
    status = models.ForeignKey(Status,
                               on_delete=models.PROTECT,
                               verbose_name=_('Status'))
    executor = models.ForeignKey(CustomUser,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 blank=True,
                                 related_name='tasks_to_do',
                                 verbose_name=_('Executor'))
    labels = models.ManyToManyField(Label,
                                    through='LabelRelationTask',
                                    blank=True,
                                    verbose_name=_('Labels'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LabelRelationTask(models.Model):
    label = models.ForeignKey(Label,
                              on_delete=models.PROTECT,
                              null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
