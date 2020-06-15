DEFAULT_CURRENCY = 'EUR'
DATA_FOLDER = 'data'


CURRENCY = {
    'EUR': {
        'namespace': ('euro', 'eur'),
    },
    'USD': {
        'namespace': ('dollar', 'usd'),
    }
}


COLUMNS = {
    'handlers': {
        'datetime': {
            'namespace': ('timestamp', 'date', 'date_readable'),
            '_class': 'DateTime'
        },
        'transaction': {
            'namespace': ('type', 'transaction'),
        },
        'amount': {
            'namespace': ('amounts', 'amount', 'cents'),
            '_class': 'Amount',
        },
        'cents': {
            'namespace': ('cents',),
            '_class': 'Cents',
            'require': 'amount'
        },
        'currency': {
            'namespace': ('euro', 'eur', 'dollar', 'usd'),
            '_class': 'Currency',
            'require': 'amount'
        },
        'from': {
            'namespace': ('sender', 'from'),
        },
        'to': {
            'namespace': ('reciever', 'to'),
        },
    },

    'columns': {
        'datetime':{
            'handler': 'datetime',
            'position': 1
        },
        'datetime_hr': {
            'handler': 'datetime',
            'formatter': '',
            'position': 2
        },
        'transaction_type': {
            'handler': 'transaction',
            'position': 3
        },
        'amount': {
            'handler': 'amount',
            'position': 4
        },
        'currency': {
            'handler': 'currency',
            'position': 5
        },
        'from': {
            'handler': 'from',
            'position': 6
        },
        'to': {
            'handler': 'to',
            'position': 7
        }
    }
}