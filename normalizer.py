import re


def normalize(pair):
    # выбрасывает знаки препинания, если они не стоят рядом с числами
    query_str = pair[0]
    completion_str = pair[1]
    for sym in ['"', '#', '\$', '\&', '\+',
                '\*', '\?', '@',
                '\^', '_', '`', '\|', '~',
                '«', '»', '\!', '%', ',', '\.',
                '\:', ';', '<', '=', '>']:
        if not (re.search('\d'+sym+'\d', query_str) or
                re.search('\d'+sym+'\d', completion_str)):
            query_str = re.sub(sym, ' ', query_str)
            completion_str = re.sub(sym, ' ', completion_str)
    for sym in '()[]{}/\\':
        query_str = query_str.replace(sym, ' ')
        completion_str = completion_str.replace(sym, ' ')
        query_str, completion_str = query_str.strip(), completion_str.strip()

    return query_str, completion_str
