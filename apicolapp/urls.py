from django.contrib import admin
from django.contrib import auth
from django.urls import path, include

from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('apiarios/', include('apiary.urls')),
    path('gestion/', include('accounting.urls')),
    # path('user/', include('user_manager.urls')),
]
