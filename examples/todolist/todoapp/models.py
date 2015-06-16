from django.db import models

# Create your models here.

class TaskBoard(models.Model):
    title = models.CharField(max_length=50)


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    task_board = models.ForeignKey('TaskBoard', related_name='task_set')
