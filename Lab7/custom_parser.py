import re

REGEXP = '\[\s*[0-9]*\]\s*[0-9\.-]*\s*(sec)\s*[0-9\.]*\s*[A-Z]?(Bytes)\s*[0-9\.]*\s*[A-Z]?(bits/sec)'
KEYS = ('Interval', 'Transfer', 'Bandwidth')


def parse(input: str):
    regex = r'\[\s*\d+\]\s*([\d.-]+)\s*sec\s*([\d.]+)\s*([KMGT]?Bytes)\s*([\d.]+)\s*([KMGT]?bits/sec)\s*'
    keys = ('Interval', 'Transfer', 'Bandwidth')

    matches = re.findall(regex, input)

    result = []
    for match in matches:
        values = {
            'Interval': match[0],
            'Transfer': match[1],
            'Bandwidth': match[3],
        }
        result.append(values)

    return result[:-2]
