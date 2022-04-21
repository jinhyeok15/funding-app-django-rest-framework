from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.PostItemView.as_view())
]
