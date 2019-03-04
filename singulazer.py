import re


def choose_best(outname_restored, outname_tofix):
    for filename in [outname_restored, outname_tofix]:
        outname = re.sub('_[a-z]+.csv', '.csv', filename)
        outfile = open(outname, 'w', encoding='utf-8')

        hashed_queries = {}

        file = open(filename, 'r', encoding='utf-8')
        for line in file:
            weight, query = int(line.split('\t')[0]), line.split('\t')[1]
            hashed = hash(query)
            if hashed not in hashed_queries.keys():
                hashed_queries[hashed] = weight
                outfile.write(line)
            else:
                if hashed_queries[hashed] < 0:
                    pass
