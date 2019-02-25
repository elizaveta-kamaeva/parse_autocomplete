import re
from time import time
import pandas as pd
from matchbox import Matchbox


def get_compare_data(filename):
    filepath = 'infiles\\' + filename
    df = pd.read_csv(filepath, sep=';', dtype=str, error_bad_lines=False)
    df = df.fillna('NULL')
    qu_au_list = df.apply(tuple, axis=1).tolist()

    print('{} queries from {} found.'.format(len(qu_au_list),filename))
    return qu_au_list


def get_feed(filename):
    filepath = 'infiles\\' + filename
    text_list = open(filepath, 'r', encoding='utf-8').readlines()
    text = ''
    for line in text_list:
        text += re.sub('<.+?>', ' ', line, flags=re.DOTALL) + '\n'
    feed_set = set()
    for item in re.split('[\W_]+', text):
        if item and \
                not (re.match('full_', item) or
                     re.fullmatch('\d+', item)):
            feed_set.add(item.lower())

    print('{} unique feed words from {} found.'.format(len(feed_set), filename))
    return feed_set


def write_file(outname, tuple_set):
    outfile = open(outname, 'w', encoding='utf-8')
    outfile.write('{}\t{}\t{}\t{}\n'.format('distance', 'query', 'complete_suggestion', 'full_complete'))
    for quadrum in tuple_set:
        outfile.write('{}\t{}\t{}\t{}\n'.format(quadrum[0],
                                                quadrum[1],
                                                quadrum[2],
                                                quadrum[3]))
    outfile.close()


filename = 'yazapros.csv'
feed_name = 'export_full_all_1.xml'
outname_restored = 'outfiles\\' + filename.split('.')[0] + '-dataset_restored-1.csv'
outname_tofix = 'outfiles\\' + filename.split('.')[0] + '-dataset_tofix-1.csv'

query_completion_list = get_compare_data(filename)
# feed = get_feed(feed_name)
feed = set()

matches_obj = Matchbox(query_completion_list, feed)
t = time()
Matchbox.collect_matches(matches_obj)

write_file(outname_restored, matches_obj.restored)
write_file(outname_tofix, matches_obj.tofix_manually)

seconds = round(time() - t)
print('Process took {0} minute{2} {1} seconds.'.format(seconds // 60, seconds % 60, '' if seconds // 60 == 1 else 's'))
