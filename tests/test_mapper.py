import csv
from datetime import datetime

import pytest


@pytest.mark.parametrize('input, expected', [
    ({'date': '03-10-2019', 'amounts': '2123.99'},
     {'datetime': datetime(2019, 10, 3).isoformat(), 'amount': 2123.99, 'currency': None}),
    ({'date_readable': '5 Oct 2019', 'euro': '5', 'cents': '44'},
     {'datetime': datetime(2019, 10, 5).isoformat(), 'amount': 5.44, 'currency': 'EUR'}
     ),
])
def test_remap(mapper, input, expected):
    remapped = mapper.remap(input)
    assert all(remapped[k] == v for k, v in expected.items())


def test_remap_csv(mapper, files):
    headers = mapper.get_ordered_keys()

    for file in files:
        reader = csv.DictReader(file)
        for row in reader:
            assert all(k in headers for k in mapper.remap(row))
