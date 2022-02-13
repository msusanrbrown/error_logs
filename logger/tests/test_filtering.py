
from sre_constants import CATEGORY
from logger.filtering import filtering_log
import logger.logs as logs
from ..logs import process_log
from unittest.mock import MagicMock, patch, Mock, call
from io import StringIO
import logger.converter as converter

TIMESTAMP = '20211102T00:02'
APPLICATION = 'APP2'
CATEGORY = 'SUCCESS'
SEVERITY = 1

LOG = ['20211102T00:00 - APP0 - SUCCESS: No problem here.', 
        '20211102T00:01 - APP1 - INFO: Some info here.',
        '20211102T00:02 - APP2 - ERROR [1]: Non-severe',
        '20211102T00:02 - APP2 - ERROR [5]: Severe',
        '20211102T00:07 - APP7 - ERROR [1]: Non-Severe',
        '20211102T00:04 - APP4 - ERROR [2]: Mild',
        '20211102T00:05 - APP5 - ERROR [3]: Less-severe',
        '20211102T00:06 - APP6 - ERROR [4]: Strong'
        ]

@patch('logger.converter.convert_to_string', MagicMock(return_value='hi'))
def test_filtering_log__bad_input():
    
    content = StringIO('hi')
    # content.write('hi')
    data = {'Body':content}
    query = {}
    result = filtering_log(data, query)
    # assert False
    assert result == []
    assert converter.convert_to_string.call_args_list == [call(data)]


@patch('logger.converter.convert_to_string', MagicMock(return_value='\n'.join(LOG)))
def test_filtering_log__good_log__empty_query():
    
    content = StringIO('\n'.join(LOG))
    # content.write('hi')
    data = {'Body':content}
    query = {}
    result = filtering_log(data, query)
    # assert False
    assert result == LOG
    assert converter.convert_to_string.call_args_list == [call(data)]


@patch('logger.converter.convert_to_string', MagicMock(return_value='\n'.join(LOG)))
def test_filtering_log__good_log__query_by_timestamp():
    
    content = StringIO('\n'.join(LOG))
    # content.write('hi')
    data = {'Body':content}
    query = {'TIMESTAMP':TIMESTAMP}
    result = filtering_log(data, query)
    # assert False
    assert result == ['20211102T00:02 - APP2 - ERROR [1]: Non-severe',
                        '20211102T00:02 - APP2 - ERROR [5]: Severe']
    assert converter.convert_to_string.call_args_list == [call(data)]


@patch('logger.converter.convert_to_string', MagicMock(return_value='\n'.join(LOG)))
def test_filtering_log__good_log__query_by_app():
    
    content = StringIO('\n'.join(LOG))
    # content.write('hi')
    data = {'Body':content}
    query = {'APPLICATION':APPLICATION}
    result = filtering_log(data, query)
    # assert False
    assert result == ['20211102T00:02 - APP2 - ERROR [1]: Non-severe',
                        '20211102T00:02 - APP2 - ERROR [5]: Severe']
    assert converter.convert_to_string.call_args_list == [call(data)]


@patch('logger.converter.convert_to_string', MagicMock(return_value='\n'.join(LOG)))
def test_filtering_log__good_log__query_by_category():
    
    content = StringIO('\n'.join(LOG))
    # content.write('hi')
    data = {'Body':content}
    query = {'CATEGORY': CATEGORY}
    result = filtering_log(data, query)
    # assert False
    assert result == ['20211102T00:00 - APP0 - SUCCESS: No problem here.']
    assert converter.convert_to_string.call_args_list == [call(data)]


@patch('logger.converter.convert_to_string', MagicMock(return_value='\n'.join(LOG)))
def test_filtering_log__good_log__query_by_severity():
    
    content = StringIO('\n'.join(LOG))
    # content.write('hi')
    data = {'Body':content}
    query = {'SEVERITY': SEVERITY}
    result = filtering_log(data, query)
    # assert False
    assert result == ['20211102T00:02 - APP2 - ERROR [1]: Non-severe', 
                    '20211102T00:07 - APP7 - ERROR [1]: Non-Severe']
    assert converter.convert_to_string.call_args_list == [call(data)]


@patch('logger.converter.convert_to_string', MagicMock(return_value='\n'.join(LOG)))
def test_filtering_log__good_log__query_by_all():
    
    content = StringIO('\n'.join(LOG))
    # content.write('hi')
    data = {'Body':content}
    query = {'TIMESTAMP':TIMESTAMP, 'APPLICATION':APPLICATION, 'CATEGORY': 'ERROR', 'SEVERITY': SEVERITY}
    result = filtering_log(data, query)
    # assert False
    assert result == ['20211102T00:02 - APP2 - ERROR [1]: Non-severe']
    assert converter.convert_to_string.call_args_list == [call(data)]