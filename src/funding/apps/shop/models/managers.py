from django.db import models


class ParticipantManager(models.Manager):
    def filter(self, is_join=None, **kwargs):
        if is_join is None:
            return super().filter(is_join=True, **kwargs)
        return super().filter(is_join=is_join, **kwargs)
