import re
from repuncter import restore_punctuation
from checker import can_write


class Agregator:
    def __init__(self, known_completions):
        self.known_completions = known_completions
        self.restored = set()
        self.tofix_manually = set()

    def agregate_matches(self, max_obj):
        # ПИШЕТ СЛОВА В МАССИВЫ
        query_weight = max_obj.weight
        query = max_obj.query
        complete_piece = max_obj.complete
        init_completion = max_obj.init_str

        if can_write(query, complete_piece):
            if query in self.known_completions.keys():
                # восстанавливает знаки препинания
                restored_tuple = restore_punctuation(query, self.known_completions[query])
                if restored_tuple:
                    # если запрос уже встречался, но расстояние там было больше,
                    # то заменяет на пару с меньшим весом
                    if self.known_completions[query] != restored_tuple:
                        if query_weight < self.known_completions[query][0]:
                            prev_tuple = self.known_completions[query]
                            self.known_completions[query] = restored_tuple

                            if (prev_tuple[0], query, prev_tuple[1], prev_tuple[2]) in self.restored:
                                self.restored.remove((prev_tuple[0], query,
                                                      prev_tuple[1], prev_tuple[2]))
                            self.restored.add((query_weight, query,
                                               restored_tuple[2], init_completion))
                # если не получилось восстановить пунктуацию
                else:
                    self.known_completions[query] = (query_weight,
                                                          init_completion,
                                                          complete_piece)
                    self.tofix_manually.add((query_weight, query,
                                             complete_piece, init_completion))

            # если такого исправления еще не встречалось
            else:
                restored_tuple = restore_punctuation(query,
                                                     (query_weight, init_completion, complete_piece))
                if restored_tuple:
                    self.known_completions[query] = restored_tuple
                    self.restored.add((query_weight, query,
                                       restored_tuple[2], init_completion))
                # если не получилось восстановить пунктуацию
                else:
                    self.known_completions[query] = (query_weight,
                                                     init_completion,
                                                     complete_piece)
                    self.tofix_manually.add((query_weight, query,
                                             complete_piece, init_completion))
