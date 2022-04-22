from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.ShopPostItemView.as_view())
]
