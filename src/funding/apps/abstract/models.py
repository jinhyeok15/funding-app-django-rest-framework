from tkinter import CASCADE
from django.db import models
from funding.apps.profile.models import User


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        abstract = True


class PurchaseInterface(models.Model):
    user: models.ForeignKey
    production: models.ForeignKey

    class Meta:
        abstract = True
