from . import formatter, handler


class RemappingConfig:
    """
    Defines how values will be remapped and formatted
    """
    keys: dict
    handlers: dict
    formatters: dict


class Remapper:
    """Maps values from one mapping to another using defined set of keys and value formatters"""

    def __init__(self, config: RemappingConfig):
        self._keys_map = config.keys
        self._handler = handler.Manager(config.handlers)
        self._formatter = formatter.Manager(config.formatters)

    def get_ordered_keys(self):
        """
        Get list of keys ordered by position if it's provided.
        Otherwise key is prepended from the beginning of the list
        """
        return [h[0] for h in sorted(
            self._keys_map.items(), key=lambda i: i[1].get('position', -1))]

    def remap(self, mapping: dict):
        """
        Map and format values from provided mapping to key provided in config::

            remap({'a': '1'}) -> {'my_custom_key': '1'}
        """
        _mapping = {}

        self._handler.reset_handlers()

        for col, val in mapping.items():
            self._handler.handle(col, val)

        for name, col in self._keys_map.items():
            hand_name = col.get('handler', name)
            hand = self._handler.get_handler(hand_name)
            fmt = self._formatter.get_formatter(col.get('formatter'))
            val = hand.get_val()

            if fmt:
                val = fmt.format(val)

            _mapping[name] = val

        return _mapping
