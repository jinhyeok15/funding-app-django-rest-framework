from django.urls import include, re_path, path
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('shop/', include('funding.apps.shop.urls')),
    path('user/', include('funding.apps.profile.urls')),
]
