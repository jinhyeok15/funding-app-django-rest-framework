"""
AbstractModel 중에 필드명은 동일하게 가져가지만 구현부분이 다른 모델은 여기에 정의한다.
"""


from django.db import models


class PurchaseAbstractModel(models.Model):
    """
    유저(user)와 품목(production)을 abstract로 상속하여 받는다
    """
    user_id: models.ForeignKey
    production: models.ForeignKey

    class Meta:
        abstract = True
