from django.urls import path
from . import views

urlpatterns = [
    path('v1/post/', views.ShopPostItemView.as_view()),
    path('v1/<int:post_id>/want_participate/', views.ShopWantParticipateView.as_view()),
]
