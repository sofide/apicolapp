import datetime

import pytest

from apiary.models import Apiary, ApiaryStatus, Harvest


def test_apiary_fields():
    """Check if are defined the needed fields in Apiary model."""
    assert hasattr(Apiary._meta.model, 'label')
    assert hasattr(Apiary._meta.model, 'status')
    assert hasattr(Apiary._meta.model, 'owner')


def test_apiary_status_fields():
    """Check if are defined the needed fields in ApiaryStatus model."""
    assert hasattr(ApiaryStatus._meta.model, 'apiary')
    assert hasattr(ApiaryStatus._meta.model, 'date')
    assert hasattr(ApiaryStatus._meta.model, 'nucs')
    assert hasattr(ApiaryStatus._meta.model, 'hives')


def test_harvest_fields():
    """Check if are defined the needed fields in Harvest model."""
    assert hasattr(Harvest._meta.model, 'apiary')
    assert hasattr(Harvest._meta.model, 'amount')
    assert hasattr(Harvest._meta.model, 'date')


def test_new_apiary_creates_a_status_instance(manolo_user):
    apiary = Apiary.objects.create(label='new apiary', owner=manolo_user)

    assert isinstance(apiary.status, ApiaryStatus)


def test_apiary_not_save_without_status(manolo_user):
    """Prevent an apiary to be saved without an status."""
    apiary = Apiary.objects.create(label='new apiary', owner=manolo_user)
    apiary_status, created = ApiaryStatus.objects.update_or_create(
        apiary=apiary,
        date=datetime.datetime.today(),
        defaults={'nucs':15, 'hives':20}
    )

    apiary.status = None
    apiary.save()

    assert apiary.status == apiary_status
