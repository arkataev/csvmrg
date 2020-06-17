## CSV Merger Utility

Using this utility you can easily merge multiple .csv files into a single stream or .csv file.

### Requirements
* Python 3.7

### Installing and Using
```bash
pip install -r requirements.txt --target csvmrg

python csvmrg {path_to_csv_folder} [--output] [--settings]
``` 

### Example
```bash
python csvmrg tests/data --output csv  
```
Merge csv files from `tests/data` folder into a single .csv file and save it into current directory

```bash
python csvmrg tests/data > data.txt
```
Pass merge output into data.txt files

```bash
python csvmrg tests/data | python my_script.py
```
Pass merge output into python script as input data

```bash
python csvmrg tests/data --settings=custom_settings.py
```
Use custom parsing configuration to tweak utility

### Settings

`HUMAN_READABLE_DATE` - Format date to more be more readable

`CSV_FORMAT_PARAMS` - Set custom params to read input csv files <https://docs.python.org/3/library/csv.html#csv-fmt-params>

`CURRENCY` - Mapping currencies aliases

`MAPPING` - Mapping and formatting input csv fields

```python
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
```