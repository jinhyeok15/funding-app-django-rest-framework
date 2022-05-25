from django.core.cache import cache
from funding.apps.core.exceptions import NotFoundRequiredParameterError


# keys
SHOP_POSTS_CREATED_DATA = 'shop_posts_created_data'
SHOP_POSTS_DEFAULT_DATA = 'shop_posts_default_data'

def get_ordered_cache_data(order_by):
    if order_by=='default':
        return cache.get(SHOP_POSTS_DEFAULT_DATA)
    if order_by=='created':
        return cache.get(SHOP_POSTS_CREATED_DATA)
    raise NotFoundRequiredParameterError('order_by')

# decorators
def shop_post_cache_on_update(func):
    def wrapper(self, *args, **kwargs):
        cache.set(SHOP_POSTS_DEFAULT_DATA, None)
        cache.set(SHOP_POSTS_CREATED_DATA, None)
        return func(self, *args, **kwargs)
    return wrapper
