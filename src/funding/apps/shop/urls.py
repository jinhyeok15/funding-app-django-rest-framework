from django.urls import path
from . import views

urlpatterns = [
    path('v1/post/', views.ShopPostItemView.as_view()),
    path('v1/<int:post_id>/want_participate/', views.ShopWantParticipateView.as_view()),
    path('v1/<int:post_id>/participate/', views.ShopPostParticipateView.as_view()),
    path('v1/post/<int:post_id>/', views.ShopPostDetailView.as_view()),
    path('v1/posts/', views.ShopPostsView.as_view()),
]
