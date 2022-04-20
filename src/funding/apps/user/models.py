from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None


class Pocket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="pocket")
    bank_account_type = models.CharField(max_length=50, null=True)
    is_activate = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_pocket(sender, instance, created, **kwargs):
    if created:
        Pocket.objects.create(user=instance)
