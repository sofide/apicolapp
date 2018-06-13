import pytest

from apiary.models import Apiary, ApiaryStatus, Harvest


def test_apiary_fields():
    """
    Check if are defined the needed fields in Apiary model.
    """
    assert hasattr(Apiary._meta.model, 'label')
    assert hasattr(Apiary._meta.model, 'status')
    assert hasattr(Apiary._meta.model, 'owner')


def test_apiary_status_fields():
    """
    Check if are defined the needed fields in ApiaryStatus model.
    """
    assert hasattr(ApiaryStatus._meta.model, 'apiary')
    assert hasattr(ApiaryStatus._meta.model, 'date')
    assert hasattr(ApiaryStatus._meta.model, 'nucs')
    assert hasattr(ApiaryStatus._meta.model, 'hives')


def test_harvest_fields():
    """
    Check if are defined the needed fields in Harvest model.
    """
    assert hasattr(Harvest._meta.model, 'apiary')
    assert hasattr(Harvest._meta.model, 'amount')
    assert hasattr(Harvest._meta.model, 'date')
