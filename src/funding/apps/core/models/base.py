from django.db import models
from funding.apps.user.models import User
from ..exceptions import DoesNotIncludeStatusError
from typing import List


class TimeStampBaseModel(models.Model):
    """
    created_at: 생성일자
    updated_at: 수정일자
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusManager(models.Manager):
    def get(self, **kwargs):
        if 'status' not in kwargs.keys():
            raise DoesNotIncludeStatusError()
        return super().get(**kwargs)


class StatusBaseModel(TimeStampBaseModel):
    status: models.CharField
    objects = StatusManager()

    class Meta:
        abstract = True


class ItemBaseModel(TimeStampBaseModel):
    """
    tag = models.CharField(max_length=256, null=True, help_text="아이템 설명 태그")
    price = models.IntegerField()
    created_at: 생성일자
    updated_at: 수정일자
    """
    tag = models.CharField(max_length=256, null=True, help_text="아이템 설명 태그")
    price = models.IntegerField()

    class Meta:
        abstract = True


class PostBaseModel(TimeStampBaseModel):
    """
    poster: 게시자
    title: 글 제목
    content: 글 내용
    created_at: 생성일자
    updated_at: 수정일자
    """
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)

    class Meta:
        ordering = ['created_at']
        abstract = True
