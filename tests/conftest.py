import os

import pytest

from src.handler import Manager
from src.mapper import Remapper, RemappingConfig
from . import settings


@pytest.fixture
def handler():
    m = Manager(settings.MAPPING['handlers'])
    yield m
    m.reset_handlers()


@pytest.fixture
def mapper():
    conf = RemappingConfig()
    conf.handlers = settings.MAPPING['handlers']
    conf.keys = settings.MAPPING['keys']
    conf.formatters = settings.MAPPING['formatters']

    return Remapper(conf)


@pytest.fixture
def files():
    files = (open(entry.path) for entry in os.scandir(settings.DATA_FOLDER))
    yield files

    for f in files:
        f.close()
