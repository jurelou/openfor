import os
import sys
import inspect
import pkgutil
from importlib import import_module
import traceback

from loguru import logger


def _discover_packages(path: str):
    for (_, name, ispkg) in pkgutil.iter_modules([path]):
        pkg_path = os.path.join(path, name)
        if ispkg:
            yield from _discover_packages(pkg_path)
            continue
        if pkg_path.startswith('./'):
            pkg_path = pkg_path[2:]
        yield pkg_path.replace('/', '.')

def _import_module(mod_path: str):
    if mod_path in sys.modules:
        return sys.modules[mod_path]    
    try:
        return import_module(mod_path)
    except Exception as err:
        traceback.print_exc(file=sys.stdout)
        logger.critical(f'Could not import module {mod_path}: {err}')
    return None

def load_classes(root_path: str, parent_class):
    """Find all classes in a directory recursively."""
    modules = []
    for mod_path in _discover_packages(root_path):
        module = _import_module(mod_path)
        if not module:
            continue
        for _, mod_cls in inspect.getmembers(module, inspect.isclass):
            if (
                mod_cls.__module__.startswith(mod_path)
                and issubclass(mod_cls, parent_class)
                and parent_class != mod_cls
            ):
                modules.append(mod_cls)
    return modules