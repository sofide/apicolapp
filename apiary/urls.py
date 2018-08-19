from django.urls import path

from apiary import views


urlpatterns = [
    path('', views.index, name='apiary_index'),
    path('<int:apiary_pk>', views.apiary_detail, name='apiary_detail'),
    path('new/', views.apiary_abm, name='apiary_new'),
    path('edit/<int:apiary_pk>', views.apiary_abm, name='apiary_edit'),
    path('cargar_cosecha/', views.harvest, name='harvest_new'),
    path('editar_cosecha/<int:harvest_pk>', views.harvest, name='harvest_edit'),
    path('cosechas/', views.harvest_list, name='harvest_list'),
]
