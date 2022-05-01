from django.db import models


class ParticipantManager(models.Manager):
    """
    filter에서 is_join을 포함하지 않을 경우, is_join=True를 조회한다.
    """
    def filter(self, is_join=None, **kwargs):
        if is_join is None:
            return super().filter(is_join=True, **kwargs)
        return super().filter(is_join=is_join, **kwargs)
