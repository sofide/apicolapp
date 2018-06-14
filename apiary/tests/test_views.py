import pytest

from django.urls import reverse

from apiary.models import Apiary


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
    Test if manolo's apiaries are sent to template.
    """
    response = client_logged_as_manolo.get(reverse('apiary_index'))

    assert 'apiaries' in response.context

    assert len(response.context['apiaries']) == the_twenty_apiaries_of_manolo.count()
    assert the_twenty_apiaries_of_manolo.first().label in str(response.content)


def test_new_apiary_is_working(client_logged_as_manolo):
    """
    Test if new apiary view es working.
    """
    response = client_logged_as_manolo.get(reverse('apiary_new'))

    assert response.status_code == 200


def test_new_apiary_is_redirecting_if_user_isnt_logged(client):
    """
    Test if new_apiary redirects if user is not logged.
    """
    response = client.get(reverse('apiary_new'))

    assert response.status_code == 302
    assert response.url == reverse('login')


def test_edit_apiary_is_working(client_logged_as_manolo, apiary_of_manolo):
    """
    Test if edit user's apiary view is working.
    """
    response = client_logged_as_manolo.get(reverse('apiary_edit', args=(apiary_of_manolo.pk,)))

    assert response.status_code == 200


def test_edit_apiary_of_other_user_redirects(client_logged_as_manolo, apiary_of_samuel):
    """
    Test if edit another user's apiary view is redirecting to apiary index.
    """
    response = client_logged_as_manolo.get(reverse('apiary_edit', args=(apiary_of_samuel.pk,)))

    assert response.status_code == 302
    assert response.url == reverse('apiary_index')


def test_edit_apiary_is_editing_the_apiary(client_logged_as_manolo, apiary_of_manolo):
    old_hives = apiary_of_manolo.status.hives

    response = client_logged_as_manolo.post(reverse('apiary_edit', args=(apiary_of_manolo.pk,)), {
        'label':apiary_of_manolo.label,
        'hives': old_hives + 1000,
        'nucs': apiary_of_manolo.status.nucs,
        'date': apiary_of_manolo.status.date,
    })

    new_apiary = Apiary.objects.get(pk=apiary_of_manolo.pk)

    assert response.status_code == 302
    assert response.url == reverse('apiary_index')
    assert new_apiary.status.hives == old_hives + 1000
