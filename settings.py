# Default folder path where data files are placed
HUMAN_READABLE_DATE = '%d %b %Y %H:%M:%S%z'

CSV_FORMAT_PARAMS = {
    'delimiter': ','
}

# Currencies mapping
CURRENCY = {
    'EUR': {
        'alias': ('euro', 'eur'),
    },
    'USD': {
        'alias': ('dollar', 'usd'),
    }
}


MAPPING = {
    # Defines handlers names, aliases and custom handler types
    'handlers': {
        'datetime': {
            'alias': ('timestamp', 'date', 'date_readable'),
            '_class': 'src.handler.DateTime'
        },
        'transaction': {
            'alias': ('type', 'transaction'),
        },
        'amount': {
            'alias': ('amounts', 'amount', 'cents'),
            '_class': 'src.handler.Amount',
        },
        'cents': {
            'alias': ('cents',),
            '_class': 'src.handler.Cents',
            'require': 'amount'
        },
        'currency': {
            'alias': ('euro', 'eur', 'dollar', 'usd'),
            '_class': 'src.handler.Currency',
            'require': 'amount'
        },
        'from': {
            'alias': ('sender', 'from'),
        },
        'to': {
            'alias': ('reciever', 'to'),
        },
    },
    # Defines formatters names, aliases and custom handler types
    'formatters': {
        'datetime_hr': {
            '_class': 'src.formatter.DateReadableFormatter'
        },
        'datetime_iso': {
            '_class': 'src.formatter.DateISOFormatter'
        }
    },
    # Defines ouput mapping keys and how values will be handled and formatted
    'keys': {
        'datetime':{
            'handler': 'datetime',
            'formatter': 'datetime_iso',
            'position': 1
        },
        'datetime_hr': {
            'handler': 'datetime',
            'formatter': 'datetime_hr',
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
