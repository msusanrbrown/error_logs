import re
import logger.converter as converter
from logger.patterns import PATTERN, PATTERN_SEVERITY


def filtering_log(data, query):
    content = converter.convert_to_string(data)
    result = []
    lines = content.split('\n')
    for line in lines:
        if not line:
            continue
        found = re.search(PATTERN, line)
        if not found:
            continue
        if 'TIMESTAMP' in query and found.group(1) != query['TIMESTAMP']:
            continue
        if 'APPLICATION' in query and found.group(2) != query['APPLICATION']:
            continue
        if 'CATEGORY' in query and found.group(3) != query['CATEGORY']:
            continue

        if 'SEVERITY' in query:
            found = re.search(PATTERN_SEVERITY, line)
            if not found:
                continue
            if int(found.group(4)) != query['SEVERITY']:
                continue
       
        result.append(line)
    return result


        

    return result
