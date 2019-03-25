import re


class Repuncter():
    def __init__(self):
        self.repunction_result = ()
        self.punctuation_restored = False

    def restore_punctuation(self, query, candidate_tuple):
        weight = candidate_tuple[0]
        init_completion = candidate_tuple[1]
        complete_piece = candidate_tuple[2]
        repuncted = ''

        # pure_query_words = re.findall('[a-zа-яёĀ-ɏà-ž]+|\d+', query, flags=re.IGNORECASE)
        # pure_complete_words = re.findall('[a-zа-яёĀ-ɏà-ž]+|\d+', complete_piece, flags=re.IGNORECASE)
        pure_query_words = re.findall('[^\d\W_]+|\d+', query, flags=re.IGNORECASE)
        pure_complete_words = re.findall('[^\d\W_]+|\d+', complete_piece, flags=re.IGNORECASE)
        pure_query_separators = []
        prev_part = pure_query_words[0]

        # ищет промежуток между двумя словами + вся предыдущая часть запроса
        # вынимает предыдущую часть и следующее слово, оставляя только найденный промежуток

        for i in range(1, len(pure_query_words)):
            try:
                prevNsepNnextword = re.search(prev_part +
                                     '[\W_]*' +
                                     pure_query_words[i], query)
                prevNsepNnextword = prevNsepNnextword.group()
                prev_deleted = re.sub(prev_part, '', prevNsepNnextword, count=1)
                # sep = re.sub('[a-zа-яёA-ZА-ЯЁĀ-ɏà-ž\d]+', '', prev_deleted)
                sep = re.sub('[^_\W]+', '', prev_deleted)

                # sep = re.sub(prev_part, '', re.sub('[a-zа-яёA-ZА-ЯЁĀ-ɏà-ž\d]+', '',
                #              re.search(prev_part + pure_query_words[i] + '[\W_]*' + pure_query_words[i+1],
                #                        query).group(),
                #              flags=re.IGNORECASE), count=1)
                pure_query_separators.append(sep)
                prev_sep = sep
                # если предыдущий разделитель - спецзнак в RE, то экранирует его
                if prev_sep and prev_sep in '+*?.$+*?^|.':
                    prev_sep = '\\' + prev_sep
                prev_part += prev_sep + pure_query_words[i]

            except AttributeError:
                raise AttributeError('Symbols were processed incorrectly.\n'
                      'Parsed separators: {}\n'
                                     'Remembered part: "{}"\n'
                      'Query list: {}\n'
                      'Proposed completion: "{}"\n'
                      'Parsed completion: "{}"'.format(pure_query_separators,
                                                       prev_part,
                                                     pure_query_words,
                                                     init_completion,
                                                     complete_piece))
        # если запрос - это одно слово, то разделитель - пустая строка
        if not pure_query_separators:
            pure_query_separators = ['']

        # если можно расставить знаки препинания, то расставляет и возвращает TRUE
        # иначе возвращает все, как было, и FALSE
        if len(pure_query_words) == len(pure_complete_words):
            for i in range(len(pure_complete_words)-1):
                repuncted += pure_complete_words[i]
                repuncted += pure_query_separators[i]
            repuncted += pure_complete_words[-1]

            self.repunction_result = (weight, init_completion, complete_piece)
            self.punctuation_restored = True
        else:
            self.repunction_result = (weight, init_completion, repuncted)
