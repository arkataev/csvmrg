from handler import HandlerManager
import settings


class Mapper:

    def __init__(self):
        self._handler = HandlerManager()
        self._formatter = None

    def map_row(self, row):
        self._handler.create_handlers()

        for col, val in row:
            self._handler.handle_val(col, val)

        _row = [None] * len(settings.COLUMNS['columns'])

        for col in settings.COLUMNS['columns'].values():
            hand_name = col['handler']
            hand = self._handler.handlers[hand_name]

            pos = col.get('position', -1)

            _row[pos if pos < 0 else pos - 1] = hand.get_val() # TODO:: Apply formatter

        return _row