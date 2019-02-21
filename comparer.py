import re
from jellyfish._jellyfish import damerau_levenshtein_distance as damerau_levenshtein
from customTypes import MatchData


class Compare:

    def __init__(self, query_str, completion_str, init_str):
        self.query_str = query_str
        self.completion_str = completion_str
        self.init_str = init_str
        self.max_obj = MatchData

    def calculate_weight(self):
        query_str = re.sub('\s{2,}', ' ', self.query_str.lower())
        completion_str = re.sub('\s{2,}', ' ', self.completion_str.lower())
        query_list, completion_list = query_str.split(), completion_str.split()

        # проверяет, есть ли в строке подсказок еще какие-то слова
        if len(query_list) < len(completion_list):
            weight_completepiece_dict = {}

            # проверяет, не написано ли слово в неправильной раскладке
            if not (re.fullmatch('[a-zA-Z\W]+', query_str) and
                    re.fullmatch('[а-яА-ЯёЁ]+', completion_str)):

                # ходит по строке подсказок окном длиной в кол-во слов в запросе
                for i in range(len(completion_list) - len(query_list)):
                    complete_piece = ' '.join(completion_list[i:i + len(query_list)])

                    distance = damerau_levenshtein(query_str, complete_piece)
                    weight_completepiece_dict[distance] = complete_piece

                # клеит слова в подсказках на тот случай, если в запросе ненужные пробелы
                for i in range(len(completion_list)):
                    for j in range(i + 1, len(completion_list) + 1):
                        complete_piece = ''.join(completion_list[i:j])
                        distance = damerau_levenshtein(query_str, complete_piece)
                        weight_completepiece_dict[distance] = ' '.join(completion_list[i:j])

                # клеит слова в запросе и высчитывает вероятность схожести со склееными словами в подсказке
                query_str = ''.join(query_list)
                for i in range(len(completion_list)):
                    for j in range(i + 1, len(completion_list) + 1):
                        complete_piece = ''.join(completion_list[i:j])
                        distance = damerau_levenshtein(query_str, complete_piece)
                        weight_completepiece_dict[distance] = ' '.join(completion_list[i:j])

            if weight_completepiece_dict:
                max_weight = min(weight_completepiece_dict.keys())
                self.max_obj.weight = max_weight
                self.max_obj.query = self.query_str
                self.max_obj.complete = weight_completepiece_dict[max_weight]
                self.max_obj.init_complete = self.init_str

        if len(query_list) == len(completion_list):
            self.max_obj.weight = damerau_levenshtein(query_str, completion_str)
            self.max_obj.query = self.query_str
            self.max_obj.complete = completion_str
            self.max_obj.init_complete = self.init_str
