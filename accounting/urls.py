from django.urls import path

from accounting import views


urlpatterns = [
    path('', views.accounting_index, name='accounting_index'),
    path('product/', views.product_index, name='product_index'),
    path('product/new/', views.product_edit, name='product_new'),
    path('edit/<int:product_pk>', views.product_edit, name='product_edit'),
    path('purchase/', views.purchase_product, name='purchase_product'),
    path('purchase/<int:product_pk>', views.purchase_detail, name='purchase_detail'),
]
