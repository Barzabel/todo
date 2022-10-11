from django.db import models
from django.contrib.auth.models import User 


class Todo(models.Model):
    titel = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    date_done = models.DateTimeField(null=True, blank=True)
    memo = models.TextField(blank=True)
    imported = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return u"{}".format(self.titel)
