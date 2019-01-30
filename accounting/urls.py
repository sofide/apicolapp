from django.urls import path

from accounting import views


urlpatterns = [
    path('', views.accounting_index, name='accounting_index'),
    path('productos/', views.product_index, name='product_index'),
    path('productos/nuevo/', views.product_edit, name='product_new'),
    path('editar/<int:product_pk>', views.product_edit, name='product_edit'),
    path('compras/', views.purchase_list, name='purchase_list'),

    # loading a purchase consists of two steps: select product and complete purchase info.
    path('compras/cargar', views.purchase_product, name='purchase_product'),
    path('compras/<int:product_pk>', views.purchase_detail, name='purchase_detail'),

    # edit purchase info
    path('compras/editar/<int:purchase_pk>/<int:product_pk>',
         views.purchase_detail, name='purchase_detail_edit'),

    path('ventas/', views.sales_list, name='sales_list'),
    path('ventas/cargar', views.sale_new, name='sale_new'),
    path('ventas/editar/<int:sale_pk>', views.sale_new, name='sale_edit'),
]
