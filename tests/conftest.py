import csv
import os

import pytest

import settings
from handler import HandlerManager


@pytest.fixture
def handler():
    return HandlerManager()


@pytest.fixture
def csv_rows():
    files = (open(entry.path) for entry in os.scandir(settings.DATA_FOLDER))
    csv_dicts = (csv.DictReader(f) for f in files)

    yield (row for reader in csv_dicts for row in reader)

    for f in files:
        f.close()