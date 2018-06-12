import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from apiary.models import Apiary, ApiaryStatus


MANOLO_USERNAME = 'manolo'
MANOLO_PASSWORD = 'password_de_manolo'


@pytest.fixture
def manolo_user(django_user_model):
    """
    Creates and returns a user with username 'manolo'.
    """
    user = django_user_model.objects.create(username=MANOLO_USERNAME)
    user.set_password(MANOLO_PASSWORD)
    user.save()

    return user


@pytest.fixture
def client_logged_as_manolo(client, manolo_user):
    """
    Returns a client logged as manolo.
    """
    client.login(username=MANOLO_USERNAME, password=MANOLO_PASSWORD)

    return client


@pytest.fixture
def the_twenty_apiaries_of_manolo(manolo_user):
    """
    Creates and returns twenty apiaries with manolo as owner.
    """
    for i in range(20):
        new_apiary = Apiary(label='Apiary #{}'.format(i), owner=manolo_user)
        new_apiary.save()

    return Apiary.objects.filter(owner=manolo_user)


def test_apiary_index_is_working(client, django_user_model):
    """
    Test if apiary_index view is working.
    """
    response = client.get('/apiary/')
    assert response.status_code == 200

    response = client.get(reverse('apiary_index'))
    assert response.status_code == 200


def test_manolo_has_apiaries(client_logged_as_manolo, the_twenty_apiaries_of_manolo):
    """
    Test if manolo's apiaries are sent to template
    """
    response = client_logged_as_manolo.get(reverse('apiary_index'))

    assert 'apiaries' in response.context

    assert len(response.context['apiaries']) == the_twenty_apiaries_of_manolo.count()
