import pytest

from django.urls import reverse

from apiary.models import Apiary

SIMPLE_VIEWS_WITH_LOGIN = [
    ('/gestion/', 'accounting_index'),
    ('/gestion/productos/nuevo/', 'product_new'),
    ('/gestion/compras/', 'purchase_list'),
    ('/gestion/ventas/', 'sales_list'),
    ('/gestion/ventas/cargar/', 'sale_new'),
]

@pytest.mark.parametrize('path,reverse_url', SIMPLE_VIEWS_WITH_LOGIN)
def test_all_simple_views_are_working(client_logged_as_manolo, path, reverse_url):
    response = client_logged_as_manolo.get(path)
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse(reverse_url))
    assert response.status_code == 200


@pytest.mark.parametrize('path,reverse_url', SIMPLE_VIEWS_WITH_LOGIN)
def test_all_simple_views_are_redirecting_if_not_user_is_not_logged(client, path, reverse_url):
    response = client.get(path)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

    response = client.get(reverse(reverse_url))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


def test_edit_product_is_working(client_logged_as_manolo, product_of_manolo):
    response = client_logged_as_manolo.get('/gestion/editar/{}/'.format(product_of_manolo.pk))
    assert response.status_code == 200

    response = client_logged_as_manolo.get(reverse('product_edit', args=(product_of_manolo.pk,)))
    assert response.status_code == 200
# PRODUCT_NEW
# TODO test its saving a new product
# TODO test if reciving next param is redirecting correctly
# TODO raise error if not logged

# PRODUCT EDIT
# TODO test its editing a new product
# TODO raise error if not logged
# TODO raise error if trying to edit another user product

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
        reverse('purchase_detail_edit', args=(product_of_manolo.pk, product_of_manolo.pk))
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


# SALES NEW
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
