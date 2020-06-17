import csv
import logging
from datetime import datetime
from typing import List

import settings
from .mapper import Remapper

logger = logging.getLogger('merger')


def remap_csvs(mapper: Remapper, *csvs):
    """
    Merges multiple .csv files in folder into single data stream with remapped keys.
    """
    remap = mapper.remap

    for file in csvs:
        reader = csv.DictReader(file, **settings.CSV_FORMAT_PARAMS)
        f_name = file.name

        logger.info(f'mapping {f_name}')

        for row in reader:
            remapped = remap(row)
            remapped['file_name'] = f_name
            yield remapped


def csv_from_dicts(fields: List[str], *dicts: dict, output: str = ''):
    """Writes mapped data to csv file"""

    if not dicts:
        logger.warning(f'No data to write .csv file')
        return

    if not output:
        _timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        output = f'{_timestamp}.csv'

    with open(output, 'w+') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writerow = writer.writerow

        for d in dicts:
            writerow(d)

    logger.info(f'CSV created: {output}')
