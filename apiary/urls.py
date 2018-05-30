from django.urls import path

from apiary import views


urlpatterns = [
    path('', views.index, name='apiary_index'),
    path('new/', views.edit_apiary, name='new_apiary'),
    path('edit/<int:apiary_pk>', views.edit_apiary, name='edit_apiary'),
]
