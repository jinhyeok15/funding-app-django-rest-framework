from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('auth/', include(([
        path('token/', obtain_auth_token, name='api_token_auth')
    ], 'user'), namespace='auth')),
    path('account/', include(([
        path('signup/', views.AccountCreate.as_view(), name='user_login')
    ], 'user'), namespace='account'))
]
