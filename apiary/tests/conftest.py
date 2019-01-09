import pytest

from django.contrib.auth.models import User

from apiary.models import Apiary, ApiaryStatus


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
def the_twenty_apiaries_of_manolo(manolo_user):
    """Creates and returns twenty apiaries with manolo as owner."""
    for i in range(20):
        new_apiary = Apiary(label='Apiary #{}'.format(i), owner=manolo_user)
        new_apiary.save()

    return Apiary.objects.filter(owner=manolo_user)


@pytest.fixture
def apiary_of_manolo(manolo_user):
    """Creates and returns twenty apiaries with manolo as owner."""
    new_apiary = Apiary.objects.create(label='Apiary of Manolo', owner=manolo_user)

    return new_apiary


@pytest.fixture
def apiary_of_samuel(samuel_user):
    """Creates and returns twenty apiaries with samuel as owner."""
    new_apiary = Apiary.objects.create(label='Apiary of Samuel', owner=samuel_user)

    return new_apiary
