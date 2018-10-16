from django.db import models
from django.contrib.auth import get_user_model 
from django.conf import settings


class Entry(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
