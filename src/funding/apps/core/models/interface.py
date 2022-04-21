from django.db import models


class PurchaseInterface(models.Model):
    user: models.ForeignKey
    production: models.ForeignKey

    class Meta:
        abstract = True