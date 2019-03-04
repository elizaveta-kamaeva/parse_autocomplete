import re


def restore_punctuation(query, candidate_tuple):
    weight = candidate_tuple[0]
    init_completion = candidate_tuple[1]
    complete_piece = candidate_tuple[2]
    repuncted = ''

    pure_query_words = re.findall('[a-zа-яёĀ-ɏà-ž]+|\d+', query, flags=re.IGNORECASE)
    pure_complete_words = re.findall('[a-zа-яёĀ-ɏà-ž]+|\d+', complete_piece, flags=re.IGNORECASE)
    pure_query_separators = []
    prev_sep = ''

    # print(init_completion)
    # ищет промежуток между двумя словами + найденный разделитель перед первым словом
    # вынимает все буквы и разделитель, оставляя только найденный промежуток
    for i in range(len(pure_query_words) - 1):
        sep = re.sub(prev_sep, '', re.sub('[a-zа-яёA-ZА-ЯЁĀ-ɏà-ž\d]+', '',
                     re.search(prev_sep + pure_query_words[i] + '[\W_]*' + pure_query_words[i+1],
                               query).group(),
                     flags=re.IGNORECASE), count=1)
        pure_query_separators.append(sep)
        prev_sep = sep
        # если предыдущий разделитель - спецзнак в RE, то экранирует его
        if prev_sep and prev_sep in '+*?.$+*?^|.':
            prev_sep = '\\' + prev_sep
    if not pure_query_separators:
        pure_query_separators = ['']

    # если можно расставить знаки препинания, то расставляет
    # иначе возвращает NONE
    if len(pure_query_words) == len(pure_complete_words):
        for i in range(len(pure_complete_words)-1):
            repuncted += pure_complete_words[i]
            repuncted += pure_query_separators[i]
        repuncted += pure_complete_words[-1]

    else:
        return None

    return weight, init_completion, repuncted
