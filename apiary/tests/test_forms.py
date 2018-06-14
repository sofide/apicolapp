import datetime

import pytest

from apiary.forms import ApiaryForm


def test_apiaryform_is_valid():
    form = ApiaryForm({
        'label': 'apiary test label',
        'hives': 300,
        'nucs': 5,
        'date': datetime.datetime.today()
    })

    assert form.is_valid()


def test_apiaryform_whitout_label_is_not_valid():
    form = ApiaryForm({
        'label': '',
        'hives': 300,
        'nucs': 5,
        'date': datetime.datetime.today()
    })

    assert not form.is_valid()
