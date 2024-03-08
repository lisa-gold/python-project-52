from django.db import models
from task_manager.users.models import Users
from django.contrib.auth.models import User
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


class Tasks(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.PROTECT,
                               related_name='tasks',
                               blank=True,
                               null=True)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT)
    executor = models.ForeignKey(Users,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 blank=True,
                                 related_name='tasks_to_do')
    labels = models.ManyToManyField(Labels,
                                    through='LabelRelationTask',
                                    null=True,
                                    blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LabelRelationTask(models.Model):
    label = models.ForeignKey(Labels,
                              on_delete=models.PROTECT,
                              null=True)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
