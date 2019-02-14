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
    feed_set = set()
    return feed_set


filename = 'googlezapros.csv'
outname = 'outfiles\\' + filename.split('.')[0] + '-dataset.csv'

query_completion_list = get_compare_data(filename)
feed = get_feed('')

matches_obj = Matchbox(query_completion_list, feed)
t = time()
Matchbox.collect_matches(matches_obj)

outfile = open(outname, 'w', encoding='utf-8')
outfile.write('{}\t{}\t{}\t{}\n'.format('probability', 'query', 'complete_suggestion', 'full_complete'))
for quadrum in matches_obj.weight_qu_com:
    outfile.write('{}:{}=={}:-->{}'.format(quadrum[0],
                                          quadrum[1],
                                          quadrum[2],
                                          quadrum[3]) + '\n')
outfile.close()

print('Process took {} seconds.'.format(round(time() - t, 2)))
