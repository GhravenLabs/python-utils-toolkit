import logging
from utils.logger import _ColourFormatter

def test_formatting_does_not_mutate_other_handlers_record():
    record = logging.LogRecord('demo', logging.INFO, 'demo.py', 1, 'hello', (), None)
    colored = _ColourFormatter('%(levelname)s %(message)s').format(record)
    assert '\x1b[' in colored
    assert record.levelname == 'INFO'
    assert logging.Formatter('%(levelname)s %(message)s').format(record) == 'INFO hello'
