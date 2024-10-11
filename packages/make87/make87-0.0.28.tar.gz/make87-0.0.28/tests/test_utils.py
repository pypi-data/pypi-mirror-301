from unittest.mock import MagicMock
from make87.utils import _import_class_from_string, LEVEL_MAPPING, CWD
import importlib


def test_import_class_from_string(mocker):
    mock_module = MagicMock()
    mock_class = MagicMock()
    setattr(mock_module, "TimeStamp", mock_class)
    mocker.patch("importlib.import_module", return_value=mock_module)

    result = _import_class_from_string("make87_messages.datetime.timestamp.TimeStamp")
    assert result == mock_class
    importlib.import_module.assert_called_with("make87_messages.datetime.timestamp_pb2")


def test_level_mapping():
    assert LEVEL_MAPPING["DEBUG"] == 10
    assert LEVEL_MAPPING["INFO"] == 20
    assert LEVEL_MAPPING["WARNING"] == 30
    assert LEVEL_MAPPING["ERROR"] == 40
    assert LEVEL_MAPPING["CRITICAL"] == 50


def test_cwd():
    import os

    assert CWD == os.getcwd()
