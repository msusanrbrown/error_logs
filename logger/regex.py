import re

PATTERN = r'^(\d{8}T\d{2}:\d{2}) - (\w+) - (\w+)( \[\d\])?: (.+)$'

result = re.search(PATTERN, '20211102T00:02 - APP - ERROR [1]: Non-severe')

# result = re.search(PATTERN, '20211102T00:00 - APP - SUCCESS: No problem here.')

print(result)