import re
from comparer import Compare
from checker import Checker
from normalizer import normalize
from repuncter import restore_punctuation


class Matchbox:
    def __init__(self, query_completion_list, feed_set):
        self.query_completion_list = query_completion_list
        self.feed_set = feed_set

        self.restored = set()
        self.tofix_manually = set()

    def collect_matches(self):
        check_obj = Checker(self.feed_set)
        known_completions = {}

        n = 0
        for pair in self.query_completion_list:
            init_str = pair[1]
            query_str, completion_str = normalize(pair)

            # пропускает, если подсказок нет или запрос - это не буквы
            if completion_str == 'NULL' or re.fullmatch('\W+', query_str):
                n += 1
                if n % 3000 == 0:
                    print(n, 'lines processed')
                continue

            compare_obj = Compare(query_str, completion_str)
            Compare.calculate_weight(compare_obj)
            query_weight = compare_obj.max_obj.weight
            query = compare_obj.max_obj.query
            complete_piece = compare_obj.max_obj.complete
            init_completion = init_str

            # выбирает пары с нужным расстоянием Левенштейна
            if 0 <= query_weight <= 2:
                if not Checker.words_in_feed(check_obj, complete_piece, query):
                    if query in known_completions.keys():

                        # восстанавливает знаки препинания
                        restored_tuple = restore_punctuation(query, known_completions[query])
                        if restored_tuple:
                            if known_completions[query] != restored_tuple:
                                if query_weight < known_completions[query][0]:
                                    known_completions[query] = restored_tuple
                                    self.restored.add((query_weight, query,
                                                       restored_tuple[2], init_completion))
                        # если не получилось восстановить пунктуацию
                        else:
                            known_completions[query] = (query_weight, init_completion, complete_piece)
                            self.tofix_manually.add((query_weight, query, complete_piece, init_completion))

                    # если такого исправления еще не встречалось
                    else:
                        restored_tuple = restore_punctuation(query, (query_weight, init_completion, complete_piece))
                        if restored_tuple:
                            known_completions[query] = restored_tuple
                            self.restored.add((query_weight, query,
                                               restored_tuple[2], init_completion))
                        # если не получилось восстановить пунктуацию
                        else:
                            known_completions[query] = (query_weight, init_completion, complete_piece)
                            self.tofix_manually.add((query_weight, query, complete_piece, init_completion))

            n += 1
            if n % 3000 == 0:
                print(n, 'lines processed')

        print('Total number of lines:', n)
