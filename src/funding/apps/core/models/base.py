from django.db import models
from funding.apps.user.models import User


class TimeStampBaseModel(models.Model):
    """
    created_at: 생성일자
    updated_at: 수정일자
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
