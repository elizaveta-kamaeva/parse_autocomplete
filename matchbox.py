import re
from comparer import Compare
from checker import Checker


class Matchbox:
    def __init__(self, query_completion_list, feed_set):
        self.query_completion_list = query_completion_list
        self.feed_set = feed_set

        self.weight_qu_com = set()

    def collect_matches(self):
        check_obj = Checker(self.feed_set)
        known_completions = {}

        n = 0
        for pair in self.query_completion_list:
            init_str = pair[0]
            query_str = re.sub('\S*\d+(\S*\d+)*\S*', '', pair[0], flags=re.I)
            completion_str = re.sub('\S*\d+(\S*\d+)*\S*', '', pair[1], flags=re.I)
            for sym in '!"#$%&()*+,./:;<=>?@[\]^_`{|}~«»№':
                query_str = query_str.replace(sym, ' ')
                completion_str = completion_str.replace(sym, ' ')
                query_str, completion_str = query_str.strip(), completion_str.strip()
            # пропускает, если подсказок нет или запрос - это не буквы
            if completion_str == 'NULL' or re.fullmatch('\W+', query_str):
                n += 1
                continue

            compare_obj = Compare(query_str, completion_str, init_str)
            Compare.calculate_weight(compare_obj)
            query_weight = compare_obj.max_obj.weight
            query = compare_obj.max_obj.query
            complete_piece = compare_obj.max_obj.complete
            init_completion = compare_obj.max_obj.init_complete

            # выбирает пары с нужным расстоянием Левенштейна
            if 0 <= query_weight <= 2:
                if Checker.words_in_feed(check_obj, complete_piece, query):
                    if query in known_completions:
                        if known_completions[query] != (query_weight, init_completion, complete_piece):
                            if query_weight < known_completions[query][0]:
                                known_completions[complete_piece] = (query_weight, init_completion, complete_piece)
                    else:
                        known_completions[query] = (query_weight, init_completion, complete_piece)

            n += 1
            if n % 3000 == 0:
                print(n, 'lines processed')

        for query in known_completions.keys():
            self.weight_qu_com.add((known_completions[query][0],
                                    query,
                                   known_completions[query][2],
                                   known_completions[query][1]))
        print('Total number of lines:', n)


