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
            query_str, completion_str = pair[0], pair[1]
            for sym in '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~«»':
                query_str = query_str.replace(sym, '')
                completion_str = completion_str.replace(sym, '')
                query_str, completion_str = query_str.strip(), completion_str.strip()
            # если подсказок нет или запрос - это число
            if completion_str == 'NULL' or re.fullmatch('\d+', query_str):
                n += 1
                continue

            compare_obj = Compare(query_str, completion_str)
            Compare.calculate_weight(compare_obj)
            query_weight = compare_obj.max_obj.weight
            if 1 < query_weight < 3:
                self.weight_qu_com.add((query_weight,
                                        compare_obj.max_obj.query,
                                        compare_obj.max_obj.complete,
                                        compare_obj.max_obj.init_complete))
            n += 1
            if n % 3000 == 0:
                print(n, 'lines processed')
        print('Total number of lines:', n)
