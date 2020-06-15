import logging
from collections import deque

from dateutil.parser import parse as parse_datetime

import settings


logger = logging.getLogger(__name__)


class Handler:

    def __init__(self):
        self._val = None

    def set_val(self, val):
        self._val = val

    def get_val(self):
        return self._val


class DateTime(Handler):

    def set_val(self, val):
        try:
            self._val = parse_datetime(val)
        except ValueError:
            self._val = None

class Amount(Handler):

    def __init__(self):
        super().__init__()
        self._val = 0

    def set_val(self, val):
        try:
            self._val = float(val)
        except ValueError:
            self._val = None


class Currency(Handler):

    def __init__(self, amount: Amount, *args, **kwargs):
        self.amount = amount
        self.currency_map = {j: k for k, v in settings.CURRENCY.items() for j in v['namespace']}
        super().__init__(*args, **kwargs)

    def set_val(self, val):
        try:
            val = float(val)
        except ValueError:
            curr = self.currency_map.get(val, None)
            logger.info(f'Unknown currency {val}')
            self._val = curr
        else:
            self.amount.set_val(val)


class Cents(Currency):

    def set_val(self, val):
        try:
            val = self.amount.get_val() + float(f'0.{val}')
        except ValueError:
            pass
        else:
            self.amount.set_val(val)



class HandlerManager:

    def __init__(self):
        self._column_map = {j: k for k, v in settings.COLUMNS['handlers'].items() for j in v['namespace']}
        self.handlers = {}

    def create_handlers(self):
        items = deque(settings.COLUMNS['handlers'].items())
        while items:
            k, v = items.popleft()

            # TODO:: move to method
            column = globals().get(v.get('_class', 'Handler'))
            required = v.get('require')

            if required:
                if required in self.handlers:
                    self.handlers[k] = column(self.handlers[required])
                else:
                    items.append((k, v))
            else:
                self.handlers[k] = column()

    def handle_val(self, col_name, val):
        col_name = col_name.lower()
        handler_name = self._column_map.get(col_name, col_name)
        handler = self.handlers.get(handler_name, Handler())

        handler.set_val(val)
        if type(handler) is Currency:
            handler.set_val(col_name)

        if not handler_name in self.handlers:
            self.handlers[handler_name] = handler
