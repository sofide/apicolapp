from django.urls import path

from user_manager import views


urlpatterns = [
    path('login/', views.login, name='login'),
]
