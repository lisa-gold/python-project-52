from django.db import models
from task_manager.users.models import Users
from django.contrib.auth.models import User
from task_manager.statuses.models import Statuses


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
    # labels = models.ManyToManyField(Statuses,
    # on_delete=models.SET_NULL,
    # null=True)
    created_at = models.DateTimeField(auto_now_add=True)
