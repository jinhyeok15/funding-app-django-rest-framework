from django.core.cache import cache


# keys
SHOP_POSTS_CREATED_DATA = 'shop_posts_created_data'
SHOP_POSTS_DEFAULT_DATA = 'shop_posts_default_data'
SHOP_POSTS_DEFAULT_DATA_STATUS = 'shop_posts_default_data_status'
SHOP_POSTS_CREATED_DATA_STATUS = 'shop_posts_created_data_status'

# decorators
def shop_post_cache_on_update(func):
    def wrapper(self, *args, **kwargs):
        cache.set(SHOP_POSTS_DEFAULT_DATA_STATUS, False)
        cache.set(SHOP_POSTS_CREATED_DATA_STATUS, False)
        return func(self, *args, **kwargs)
    return wrapper
