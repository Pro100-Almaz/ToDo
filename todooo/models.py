from django.db import models
from django.db.models.fields import BooleanField, DateTimeField
from django.contrib.auth.models import User

class Todo(models.Model):
    task_name = models.CharField(max_length=50)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecomplited = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name
