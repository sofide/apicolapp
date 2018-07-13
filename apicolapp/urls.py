from django.contrib import admin
from django.urls import path, include

from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('apiary/', include('apiary.urls')),
    path('accounting/', include('accounting.urls')),
    path('user/', include('user_manager.urls')),
]
