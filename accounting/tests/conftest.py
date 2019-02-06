import datetime

import pytest

from django.contrib.auth.models import User

from accounting.models import Product, Purchase, Sale, Category


MANOLO_USERNAME = 'manolo'
MANOLO_PASSWORD = 'password_de_manolo'

SAMUEL_USERNAME = 'samuel'
SAMUEL_PASSWORD = 'password_de_samuel'


@pytest.fixture
def manolo_user(django_user_model):
    """Creates and returns a user with username 'manolo'."""
    user = django_user_model.objects.create(username=MANOLO_USERNAME)
    user.set_password(MANOLO_PASSWORD)
    user.save()

    return user


@pytest.fixture
def samuel_user(django_user_model):
    """Creates and returns a user with username 'samuel'."""
    user = django_user_model.objects.create(username=SAMUEL_USERNAME)
    user.set_password(SAMUEL_PASSWORD)
    user.save()

    return user


@pytest.fixture
def client_logged_as_manolo(client, manolo_user):
    """Returns a client logged as manolo."""
    client.login(username=MANOLO_USERNAME, password=MANOLO_PASSWORD)

    return client


@pytest.fixture
def category_without_depreciation():
    category = Category.objects.create(
        label='food',
        description='category without deprecation',
        depreciation_period=0,
    )

    return category


@pytest.fixture
def product_of_manolo(manolo_user, category_without_depreciation):
    new_product = Product.objects.create(
        name='Product of Manolo',
        description='A regular product',
        user=manolo_user,
        category=category_without_depreciation
    )

    return new_product


@pytest.fixture
def purchase_of_manolo(manolo_user, product_of_manolo):
    new_purchase = Purchase.objects.create(
        product=product_of_manolo,
        date=datetime.date(2018, 1, 1),
        amount=10,
        value=100
    )

    return new_purchase


@pytest.fixture
def sale_of_manolo(manolo_user):
    new_sale = Sale.objects.create(
        date=datetime.date(2018, 1, 1),
        amount=10,
        value=100,
        description='honey sale',
        user=manolo_user
    )

    return new_sale
