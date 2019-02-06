import pytest

from django.urls import reverse

from apiary.models import Apiary

# check every url
def test_accounting_index_is_working(client_logged_as_manolo):
    response = client_logged_as_manolo.get('/gestion/')
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse('accounting_index'))
    assert response.status_code == 200


def test_product_new_is_working(client_logged_as_manolo):
    response = client_logged_as_manolo.get('/gestion/productos/nuevo/')
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse('product_new'))
    assert response.status_code == 200

# TODO test its saving a new product
# TODO test if reciving next param is redirecting correctly
# TODO raise error if not logged

def test_product_edit_is_working(client_logged_as_manolo, product_of_manolo):
    response = client_logged_as_manolo.get('/gestion/editar/{}/'.format(product_of_manolo.pk))
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse('product_edit', args=(product_of_manolo.pk,)))
    assert response.status_code == 200

# TODO test its editing a new product
# TODO raise error if not logged
# TODO raise error if trying to edit another user product

def test_purchase_list_is_working(client_logged_as_manolo):
    response = client_logged_as_manolo.get('/gestion/compras/')
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse('purchase_list'))
    assert response.status_code == 200


def test_purchase_product_is_working(client_logged_as_manolo, product_of_manolo):
    response = client_logged_as_manolo.get('/gestion/compras/cargar/')
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse('purchase_product'))
    assert response.status_code == 200


def test_purchase_product_without_product_is_redirecting(client_logged_as_manolo):
    response = client_logged_as_manolo.get('/gestion/compras/cargar/')
    assert response.status_code == 302
    assert response.url == reverse('product_new')+'?next=purchase'

    response = client_logged_as_manolo.get(reverse('purchase_product'))
    assert response.status_code == 302
    assert response.url == reverse('product_new')+'?next=purchase'


def test_purchase_detail_is_working(client_logged_as_manolo, product_of_manolo):
    response = client_logged_as_manolo.get('/gestion/compras/{}/'.format(product_of_manolo.pk))
    assert response.status_code == 200

    response = client_logged_as_manolo.get(
        reverse('purchase_detail', args=(product_of_manolo.pk,))
    )
    assert response.status_code == 200

# TODO test its saving a new purchase with the given product
# TODO raise error if not logged
# TODO raise error if trying to purchase another user product


def test_purchase_detail_edit_is_working(client_logged_as_manolo, product_of_manolo,
                                         purchase_of_manolo):
    response = client_logged_as_manolo.get(
        '/gestion/compras/editar/{}/{}/'.format(purchase_of_manolo.pk, product_of_manolo.pk)
    )
    assert response.status_code == 200

    response = client_logged_as_manolo.get(
        reverse('purchase_detail', args=(product_of_manolo.pk,))
    )
    assert response.status_code == 200

# TODO test its editing the purchase
# TODO raise error if product its not the same as the original purchase
# TODO raise error if not logged
# TODO raise error if trying to edit another user purchase


def test_purchase_delete_is_working(client_logged_as_manolo, purchase_of_manolo):
    response = client_logged_as_manolo.get(
        reverse('purchase_delete', args=(purchase_of_manolo.pk,))
    )
    assert response.status_code == 302
    assert response.url == reverse('purchase_list')

# TODO test its deleting a new purchase with the given product
# TODO raise error if not logged
# TODO raise error if trying to delete another user product


def test_sales_list_is_working(client_logged_as_manolo):
    response = client_logged_as_manolo.get('/gestion/ventas/')
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse('sales_list'))
    assert response.status_code == 200

def test_sale_new_is_working(client_logged_as_manolo):
    response = client_logged_as_manolo.get('/gestion/ventas/cargar/')
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse('sale_new'))
    assert response.status_code == 200

# TODO test its saving a new sale
# TODO raise error if not logged


def test_sale_edit_is_working(client_logged_as_manolo, sale_of_manolo):
    response = client_logged_as_manolo.get('/gestion/ventas/editar/{}/'.format(sale_of_manolo.pk))
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse('sale_edit', args=(sale_of_manolo.pk,)))
    assert response.status_code == 200

# TODO test its editing the sale
# TODO raise error if not logged
# TODO raise error if trying to edit another user sale


def test_sale_delete_is_working(client_logged_as_manolo, sale_of_manolo):
    response = client_logged_as_manolo.get(
        reverse('sale_delete', args=(sale_of_manolo.pk,))
    )
    assert response.status_code == 302
    assert response.url == reverse('sales_list')

# TODO test its deleting the sale
# TODO raise error if not logged
# TODO raise error if trying to delete another user sale
