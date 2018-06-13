import pytest

from django.urls import reverse

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


def test_new_apiary_is_working(client_logged_as_manolo):
    response = client_logged_as_manolo.get(reverse('apiary_new'))

    assert response.status_code == 200


def test_new_apiary_is_redirecting_if_user_isnt_logged(client):
    response = client.get(reverse('apiary_new'))

    assert response.status_code == 302
    assert response.url == reverse('login')


def test_edit_apiary_is_working(client_logged_as_manolo, apiary_of_manolo):
    response = client_logged_as_manolo.get(reverse('apiary_edit', args=(apiary_of_manolo.pk,)))

    assert response.status_code == 200