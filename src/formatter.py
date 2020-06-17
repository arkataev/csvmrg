from datetime import datetime
from typing import Dict

import settings
from . import utils


class Formatter:
    """Formats value to particular type and format"""
    def format(self, val):
        return val


class DateReadableFormatter(Formatter):
    """Formats date to human readable format"""

    def format(self, val: datetime):
        return val.strftime(settings.HUMAN_READABLE_DATE)


class DateISOFormatter(Formatter):
    """Formats date to ISO format"""

    def format(self, val: datetime):
        return val.isoformat()


class Manager:
    """Resolves formatters by name"""

    def __init__(self, formatters_map: dict):
        self._formatters = load_formatters(formatters_map)

    def get_formatter(self, name: str) -> Formatter:
        return self._formatters.get(name)


def load_formatters(formatters_map: dict) -> Dict[str, Formatter]:
    classes = {
        name: utils.load_from_path(params.get('_class'))
        for name, params in formatters_map.items()}

    return {name: _class() for name, _class in classes.items()}
