from django.db import models


class PurchaseAbstractModel(models.Model):
    user: models.ForeignKey
    production: models.ForeignKey

    class Meta:
        abstract = True
