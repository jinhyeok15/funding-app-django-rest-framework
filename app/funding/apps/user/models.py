from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from funding.apps.core.exceptions import DoesNotIncludeStatusError


class User(AbstractUser):
    first_name = None
    last_name = None

    class Meta:
        db_table='user'


class PocketManager(models.Manager):
    def get(self, user_id, is_active=None, **kwargs):
        if is_active is None:
            raise DoesNotIncludeStatusError
        return super().get(user_id=user_id, is_active=is_active, **kwargs)


class Pocket(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pocket", db_column="user_id")
    bank_account_type = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=False)
    objects = PocketManager()

    def update(self, bank_account_type=None, is_active=None):
        if bank_account_type is not None:
            self.bank_account_type = bank_account_type
        if is_active is not None:
            self.is_active = is_active
        self.save()
        return self


@receiver(post_save, sender=User)
def create_pocket(sender, instance, created, **kwargs):
    if created:
        Pocket.objects.create(user_id=instance)
