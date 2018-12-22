from django.urls import path

from accounting import views


urlpatterns = [
    path('', views.accounting_index, name='accounting_index'),
    path('productos/', views.product_index, name='product_index'),
    path('productos/nuevo/', views.product_edit, name='product_new'),
    path('editar/<int:product_pk>', views.product_edit, name='product_edit'),
    path('compras/', views.purchase_list, name='purchase_list'),
    path('compras/cargar', views.purchase_product, name='purchase_product'),
    path('compras/<int:product_pk>', views.purchase_detail, name='purchase_detail'),
]
