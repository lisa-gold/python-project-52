from django.db import models
from task_manager.users.models import CustomUser
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.PROTECT,
                               related_name='tasks',
                               blank=True,
                               null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(CustomUser,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 blank=True,
                                 related_name='tasks_to_do')
    labels = models.ManyToManyField(Label,
                                    through='LabelRelationTask',
                                    blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LabelRelationTask(models.Model):
    label = models.ForeignKey(Label,
                              on_delete=models.PROTECT,
                              null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
