from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.PostItem.as_view())
]
