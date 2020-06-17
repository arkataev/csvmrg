import importlib.util
import logging
import os
import sys
from argparse import ArgumentParser

logger = logging.getLogger('merger')


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.usage = "Merge and remap multiple csv files"

    parser.add_argument('path', help='Path to data folder')
    parser.add_argument('--output', help='Set merge result output', choices=['csv'])
    parser.add_argument('--debug', help='Set debug mode', action="store_true")
    parser.add_argument('--settings', help='Provide custom settings python module path')

    args = parser.parse_args()

    logger.debug(f'settings {args.settings} imported')

    if args.settings:
        spec = importlib.util.spec_from_file_location("settings", args.settings)
        settings = importlib.util.module_from_spec(spec)
        sys.modules['settings'] = settings
        spec.loader.exec_module(settings)
    else:
        import settings

    from src import mapper
    from src.services import csv_from_dicts, remap_csvs

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Debug mode: ON')

    conf = mapper.RemappingConfig()

    for k, v in settings.MAPPING.items():
        setattr(conf, k, v)

    remapper = mapper.Remapper(conf)
    data_folder = args.path

    files = []

    try:
        files = [open(entry.path) for entry in os.scandir(data_folder)]
    except FileNotFoundError:
        logger.error(f'Folder {data_folder} not found')
    else:
        remapped = remap_csvs(remapper, *files)

        if args.output == 'csv':
            headers = remapper.get_ordered_keys()
            headers.append('file_name')
            csv_from_dicts(headers, *remapped)
        else:
            for d in remapped:
                sys.stdout.write(f'{d}\n')
    finally:
        for f in files:
            f.close()
