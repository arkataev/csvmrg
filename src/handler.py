import logging
from collections import deque
from typing import Dict

from dateutil.parser import parse as parse_datetime

import settings
from . import utils

logger = logging.getLogger('merger')


class Handler:
    """
    Base handler type. Handler is used to process and store
    some input value and return processed value when asked.

    You can implement different handlers for different values
    by overriding `set_val` and `get_val` methods in inherited classes.
    """
    def __init__(self, *args, **kwargs):
        self._val = None

    def set_val(self, val):
        self._val = val

    def get_val(self):
        return self._val

    def reset(self):
        self._val = None


class Dependable:

    def __init__(self, depends: Handler, *args, **kwargs):
        self.depends = depends
        super().__init__(*args, **kwargs)


class DateTime(Handler):
    """Datetime strings handler. Tries to create datetime object from string"""
    # TODO:: Should be timezone aware

    def set_val(self, val:str):
        try:
            self._val = parse_datetime(val, fuzzy=True, dayfirst=True)
        except (ValueError, TypeError):
            self._val = None


class Amount(Handler):
    """Float numbers handler. Tries to convert input value into float number"""

    def __init__(self):
        super().__init__()
        self._val = 0

    def set_val(self, val:int):
        try:
            self._val = float(val)
        except (ValueError, TypeError):
            self._val = None


class Currency(Dependable, Handler):
    """
    Handles input values to :py:class:`Amount` if its numeric,
    or handles value on its own
    """
    def __init__(self, *args, **kwargs):
        self.currency_map = {j: k for k, v in settings.CURRENCY.items() for j in v['alias']}
        super().__init__(*args, **kwargs)

    def set_val(self, val):
        try:
            val = float(val)
        except (ValueError, TypeError):
            curr = self.currency_map.get(val, None)
            self._val = curr
        else:
            self.depends.set_val(val)


class Cents(Currency):
    """Tries to add values as fractional part to :py:class:`Amount` current value"""
    def set_val(self, val):
        try:
            val = self.depends.get_val() + float(f'0.{val}')
        except ValueError:
            pass
        else:
            self.depends.set_val(val)


class Manager:
    """
    Resolves handlers by aliases and handles values to related handler.
    """

    def __init__(self, handlers_map:dict):
        self._handlers = load_handlers(handlers_map)
        self._aliases = {j: k for k, v in handlers_map.items() for j in v['alias']}

    def get_handler(self, name:str) -> Handler:
        """Get handler by name"""
        return self._handlers.get(name, Handler())

    def resolve_alias(self, alias:str) -> Handler:
        """Get handler using its alias"""
        handler_name = self._aliases.get(alias, alias)
        return self.get_handler(handler_name)

    def handle(self, key:str, val):
        """Handle value to related handler defined by key"""
        key = key.lower()
        handler = self.resolve_alias(key)
        handler.set_val(val)

        if type(handler) is Currency:
            handler.set_val(key)
        elif type(handler) is Handler:
            self._handlers[key] = handler

        if isinstance(handler, Dependable):
            logger.debug(
                f'handled ({key},{val}) -> {(handler.get_val(), handler.depends.get_val())}')
            return

        logger.debug(f'handled ({key},{val}) -> {handler.get_val()}')

    def reset_handlers(self):
        """Set all handlers values to None or defined value"""
        for h in self._handlers.values():
            h.reset()


def load_handlers(handlers_map: dict) -> Dict[str, Handler]:
    """Create mapping with handlers names and releted instances"""

    handlers = {}
    load_queue = deque(handlers_map.items())

    classes = {
        name: utils.load_from_path(params.get('_class')) or Handler
        for name, params in handlers_map.items()}

    while load_queue:
        k, v = load_queue.popleft()
        handler = classes[k]
        required = v.get('require')

        if required:
            if required in handlers:
                handlers[k] = handler(handlers[required])
            else:
                load_queue.append((k, v))
        else:
            handlers[k] = handler()

    return handlers
