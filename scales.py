import re
from comparer import Compare
from normalizer import normalize


class Scales:
    def __init__(self, query_completion_list):
        self.query_completion_list = query_completion_list
        self.light_match = ''

    def weigh_match(self, pair):
        init_str = pair[1]
        query_str, completion_str = normalize(pair)

        # пропускает, если подсказок нет или запрос - это не буквы
        if completion_str == 'NULL' or re.fullmatch('\W+', query_str):
            return False

        compare_obj = Compare(query_str, completion_str, init_str)
        Compare.calculate_weight(compare_obj)
        query_weight = compare_obj.max_obj.weight

        # выбирает пары с нужным расстоянием Левенштейна
        if 0 <= query_weight <= 2:
            self.light_match = compare_obj.max_obj
        else:
            self.light_match = None
