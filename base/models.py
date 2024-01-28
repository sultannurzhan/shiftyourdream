from django.db import models
from django.contrib.auth.models import User

class Dream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    body = models.TextField(null=True, blank=True, max_length=1000000)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}: {self.title}'