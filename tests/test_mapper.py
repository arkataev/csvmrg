import settings
from writer import Mapper
import csv


def test_handler(csv_rows):
    header = sorted([item for item in settings.COLUMNS['columns'].items()], key=lambda i:i[1]['position'])
    header = [h[0] for h in header]
    mapper = Mapper()
    rows = map(mapper.map_row, (r.items() for r in csv_rows))

    with open('test.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(zip(header, row)))

