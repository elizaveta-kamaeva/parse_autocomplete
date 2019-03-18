import re


def can_write(query, complete_piece):
    # ПРОВЕРЯЕТ, МОЖНО ЛИ ПИСАТЬ СЛОВО
    # проверяет, оба ли слова длиннее 3 символов
    if len(query) + len(complete_piece) < 8:
        return False
    # проверяет, не состоят ли строки из цифр и знаков препинания
    elif re.fullmatch('[\W0-9_]+', query) or re.fullmatch('[\W0-9_]+', complete_piece):
        return False
    else:
        return True
