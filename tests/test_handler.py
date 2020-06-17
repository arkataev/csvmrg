from datetime import datetime

import pytest

import settings
import src.handler as _handler
from src.utils import load_from_path


def test_load_handlers():
    h = {
        'hand_c': {
            '_class': 'src.handler.Currency',
            'require': 'hand_b'
        },
        'hand_a': {
            '_class': 'src.handler.DateTime'
        },
        'hand_b': {
            '_class': 'src.handler.Amount',
        },

    }
    handlers = _handler.load_handlers(h)

    assert isinstance(handlers['hand_a'], _handler.DateTime)
    assert isinstance(handlers['hand_b'], _handler.Amount)
    assert isinstance(handlers['hand_c'], _handler.Currency)

    assert handlers['hand_c'].depends is handlers['hand_b']


@pytest.mark.parametrize('input, expected', [
    (('amount', 300), 300),
    (('amount', '300'), 300),
    (('amount', ''), None),
    (('amount', None), None),
    (('timestamp', '5 Oct 2019'), datetime(2019, 10, 5)),
    (('timestamp', '03-10-2019'), datetime(2019, 10, 3)),
    (('timestamp', 'Oct 2 2019'), datetime(2019, 10, 2)),
    (('timestamp', None), None),
    (('timestamp', ''), None),
    (('timestamp', 123), None),
    (('eur', None), 'EUR'),
    (('euro', None), 'EUR'),
    (('dollar', None), 'USD'),
])
def test_handle(handler, input, expected):
    handler.handle(*input)
    assert handler.resolve_alias(input[0]).get_val() == expected


def test_get_handler(handler):
    for name, hand in settings.MAPPING['handlers'].items():
        hand_class = load_from_path(hand.get('_class'))
        if hand_class:
            assert isinstance(handler.get_handler(name), hand_class)
        else:
            assert isinstance(handler.get_handler(name), _handler.Handler)


def test_resolve_alias(handler):
    for alias in handler._aliases:
        assert isinstance(handler.resolve_alias(alias), _handler.Handler)


@pytest.mark.parametrize('input, expected', [
    ((('euro', 300), ('cents', '44')), 300.44),
    ((('euro', 300), ('cents', None)), 300),
    ((('amount', 300), ('cents', 55)), 300.55),
])
def test_amount_handle(handler, input, expected):
    handler.handle(*input[0])
    handler.handle(*input[1])
    assert handler.get_handler('amount').get_val() == expected
