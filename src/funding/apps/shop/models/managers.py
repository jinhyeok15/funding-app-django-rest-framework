from django.db import models
from funding.apps.core.exceptions import DoesNotIncludeStatusError
from funding.apps.core.utils.backends.cache import shop_post_cache_on_update


class ShopPostManager(models.Manager):
    @shop_post_cache_on_update
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    @shop_post_cache_on_update
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @shop_post_cache_on_update
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
