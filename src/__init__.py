import logging

_logger = logging.getLogger('merger')
_handler = logging.StreamHandler()
_handler.setFormatter(fmt=logging.Formatter(fmt='%(asctime)s %(name)s [%(levelname)s] %(message)s'))
_logger.addHandler(_handler)
_logger.setLevel(logging.INFO)
