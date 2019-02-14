import re
# from fuzzywuzzy import fuzz
from jellyfish._jellyfish import damerau_levenshtein_distance as damerau_levenshtein
from customTypes import MatchData


class Compare:

    def __init__(self, query_str, completion_str):
        self.query_str = query_str
        self.completion_str = completion_str
        self.max_obj = MatchData

    def calculate_weight(self):
        query_str = re.sub('\s{2,}', ' ', self.query_str.lower())
        completion_str = re.sub('\s{2,}', ' ', self.completion_str)
        query_list, completion_list = query_str.split(), completion_str.split()

        # проверяет, есть ли в строке подсказок еще какие-то слова
        if len(query_list) < len(completion_list):
            weight_complete_piece = {}

            # ходит по строке подсказок окном длиной в кол-во слов в запросе
            for i in range(len(completion_list) - len(query_list)):
                complete_piece = ' '.join(completion_list[i:i + len(query_list)])

                # проверяет, не написано ли слово в неправильной раскладке
                if not (re.fullmatch('[a-zA-Z\W]+', query_str) and
                        re.fullmatch('[а-яА-ЯёЁ\W]+', complete_piece)):

                    # проверяет на недописанность
                    if not (re.match(query_str, complete_piece) and (len(complete_piece) - len(query_str)) > 3):
                        # fuzz_measure = fuzz.ratio(query_str, complete_piece)
                        distance = damerau_levenshtein(query_str, complete_piece)
                        weight_complete_piece[distance] = complete_piece
            if weight_complete_piece:
                max_weight = min(weight_complete_piece.keys())
                self.max_obj.weight = max_weight
                self.max_obj.query = self.query_str
                self.max_obj.complete = weight_complete_piece[max_weight]
                self.max_obj.init_complete = self.completion_str

        if len(query_list) == len(completion_list):
            # self.max_obj.weight = fuzz.partial_ratio(query_str, completion_str)
            self.max_obj.weight = damerau_levenshtein(query_str, completion_str)
            self.max_obj.query = self.query_str
            self.max_obj.complete = completion_str
            self.max_obj.init_complete = self.completion_str
