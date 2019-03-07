import os
import re
from time import time
import pandas as pd
from controller import Controller


def get_compare_data(filename):
    filepath = 'infiles\\' + filename
    df = pd.read_csv(filepath, sep=';', dtype=str, error_bad_lines=False)
    df = df.fillna('NULL')
    qu_au_list = df.apply(tuple, axis=1).tolist()

    print('{} queries from {} found.'.format(len(qu_au_list),filename))
    return qu_au_list


def remove_old():
    try:
        os.remove(outname_restored)
        os.remove(outname_tofix)
        print('Old files removed:', outname_restored, outname_tofix)
    except FileNotFoundError:
        pass


filename = 'googlezapros.csv'
outname_restored = 'outfiles\\' + filename.split('.')[0] + '-dataset_restored.csv'
outname_tofix = 'outfiles\\' + filename.split('.')[0] + '-dataset_tofix.csv'
remove_old()

t = time()
query_completion_file = open('infiles\\' + filename, 'r', encoding='utf-8')

control_obj = Controller(query_completion_file, outname_restored, outname_tofix)
control_obj.process_butches()

query_completion_file.close()

print('Total number of lines:', control_obj.n)
seconds = round(time() - t)
print('Process took {0} minute{2} {1} seconds.'.format(seconds // 60,
                                                       seconds % 60,
                                                       '' if seconds // 60 == 1 else 's'))
