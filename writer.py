class Writer:
    def __init__(self, outname_restored, outname_tofix):
        self.outname_restored = outname_restored
        self.outname_tofix = outname_tofix

        for outname in [self.outname_restored, self.outname_tofix]:
            outfile = open(outname, 'w', encoding='utf-8')
            outfile.write('{}\t{}\t{}\t{}\n'.format('distance', 'query', 'complete_suggestion', 'full_complete'))
            outfile.close()

    def write_matches(self, restored, tofix_manually):
        matches_dict = {self.outname_restored: restored, self.outname_tofix: tofix_manually}

        for outname in matches_dict:
            tuple_set = matches_dict[outname]

            outfile = open(outname, 'a', encoding='utf-8')
            for quadrum in tuple_set:
                outfile.write('{}\t{}\t{}\t{}\n'.format(quadrum[0],
                                                        quadrum[1],
                                                        quadrum[2],
                                                        quadrum[3]))
            outfile.close()