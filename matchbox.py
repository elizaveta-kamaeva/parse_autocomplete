import re
from comparer import Compare


class Matchbox:
    def __init__(self, query_completion_list, feed_set):
        self.query_completion_list = query_completion_list
        self.feed_set = feed_set

        self.weight_qu_com = set()

    def collect_matches(self):
        n = 0
        for pair in self.query_completion_list:
            query_str = re.sub('([^a-zа-яё ]+)?\d+([^a-zа-яё ]+)?(?!-?[a-zа-яё])', '', pair[0], flags=re.I)
            completion_str = re.sub('([^a-zа-яё ]+)?\d+([^a-zа-яё ]+)?(?!-?[a-zа-яё])', '', pair[1], flags=re.I)
            for sym in '!"#$%&()*+,./:;<=>?@[\]^_`{|}~«»№':
                query_str = query_str.replace(sym, '')
                completion_str = completion_str.replace(sym, '')
                query_str, completion_str = query_str.strip(), completion_str.strip()
            # пропускает, если подсказок нет или запрос - это не буквы
            if completion_str == 'NULL' or re.fullmatch('\W+', query_str):
                n += 1
                continue

            compare_obj = Compare(query_str, completion_str)
            Compare.calculate_weight(compare_obj)
            query_weight = compare_obj.max_obj.weight
            query = compare_obj.max_obj.query
            complete_piece = compare_obj.max_obj.complete
            if 3 < query_weight <= 4 and (len(query) + len(complete_piece)) >= 8:
                self.weight_qu_com.add((query_weight,
                                        compare_obj.max_obj.query,
                                        compare_obj.max_obj.complete,
                                        compare_obj.max_obj.init_complete))
            n += 1
            if n % 3000 == 0:
                print(n, 'lines processed')
        print('Total number of lines:', n)
