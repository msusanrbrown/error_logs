from distutils.log import Log
from syslog import LOG_AUTH
from ..logs import process_log
from unittest.mock import MagicMock, patch, Mock
from io import StringIO

LOG = ['20211102T00:00 - APP - SUCCESS: No problem here.', 
        '20211102T00:01 - APP - INFO: Some info here.',
        '20211102T00:02 - APP - ERROR [1]: Non-severe',
        '20211102T00:02 - APP - ERROR [5]: Severe',
        '20211102T00:02 - APP - ERROR [2]: Mild',
        '20211102T00:02 - APP - ERROR [3]: Less-severe',
        '20211102T00:02 - APP - ERROR [4]: Strong'
        ]

@patch('logger.logs.convert_to_string', MagicMock(return_value='hi'))
def test_process_log__bad_input():
    content = StringIO('hi')
    # content.write('hi')
    data = {'Body':content}
    result = process_log(data)
    # assert False
    assert result == {'ErrorCount': 0, 'SuccessCount': 0, 'Total': 0}

@patch('logger.logs.convert_to_string', MagicMock(return_value=''))
def test_process_log__no_input():
    content = StringIO('hi')
    # content.write('hi')
    data = {'Body':content}
    result = process_log(data)
    # assert False
    assert result == {'ErrorCount': 0, 'SuccessCount': 0, 'Total': 0}

@patch('logger.logs.convert_to_string', MagicMock(return_value='\n'.join(LOG)))
def test_process_log__all_info():
    content = StringIO('hi')
    # content.write('hi')
    data = {'Body':content}
    result = process_log(data)
    # assert False
    assert result == {'ErrorCount': 5, 'SuccessCount': 1, 'Total': 7}

