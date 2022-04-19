from django.contrib import admin
from .models import Item, ShopPost, ShopPurchase, Participant

admin.site.register(Item)
admin.site.register(ShopPost)
admin.site.register(ShopPurchase)
admin.site.register(Participant)
