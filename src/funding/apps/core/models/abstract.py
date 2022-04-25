"""
AbstractModel 중에 필드명은 동일하게 가져가지만 구현부분이 다른 모델은 여기에 정의한다.
"""


from django.db import models


class PurchaseAbstractModel(models.Model):
    user: models.ForeignKey
    production: models.ForeignKey

    class Meta:
        abstract = True
