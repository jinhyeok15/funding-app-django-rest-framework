from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

# urlpatterns ref here
# https://github.com/sibtc/django-multiple-user-types-example/blob/master/django_school/classroom/urls.py
urlpatterns = [
    path('auth/', include(([
        path('token/', obtain_auth_token, name='api_token_auth')
    ], 'user'), namespace='auth')),
    path('account/', include(([
        path('signup/', views.AccountCreateView.as_view(), name='user_login')
    ], 'user'), namespace='account'))
]
