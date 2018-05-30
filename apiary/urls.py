from django.urls import path

from apiary import views


urlpatterns = [
    path('', views.index, name='apiary_index'),
]
