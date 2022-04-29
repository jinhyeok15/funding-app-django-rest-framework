from django.urls import path
from . import views

urlpatterns = [
    path('v1/post/', views.ShopPostItemView.as_view()),
    path('<int:post_id>/purchase/', views.ShopPostPurchaseView.as_view()),
]
