import importlib
import os
from typing import Type
from google.protobuf.message import Message


def _import_class_from_string(path) -> Type[Message]:
    *module_path, class_name = path.split(".")
    module_name = ".".join(module_path)
    module_name += "_pb2"
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls


LEVEL_MAPPING = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}

CWD = os.getcwd()
