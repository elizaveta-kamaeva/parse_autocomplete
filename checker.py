import re


class Checker:
    def __init__(self, feed_set):
        self.feed_set = feed_set

    def words_in_feed(self, completion_str, query_str):
        # проверяет, можно ли писать слово в конечный файл

        # проверяет, оба ли слова длиннее 3 символов
        if len(query_str) + len(completion_str) < 8:
            return False

        # проверяет, есть ли слово в фиде
        can_write = False
        complete_list = re.split('[\W_]+', completion_str)
        for word in complete_list:
            word = re.sub('\d+', '', word)
            if word:
                if word in self.feed_set:
                    can_write = True
                else:
                    return False
        return can_write
