import importlib


def load_from_path(path: str):
    """Get a class from defined path string"""
    if not path:
        return

    *path, _class = path.split('.')
    m = importlib.import_module('.'.join(path))

    return getattr(m, _class)
