from scales import Scales
from agregator import Agregator
from writer import Writer


class Controller:
    def __init__(self, query_completion_file, outname_restored, outname_tofix):
        self.query_completion_file = query_completion_file

        self.n = 0
        self.reporting = 3000
        self.memory_limit = 3000
        self.last_known = {}

        self.outname_restored = outname_restored
        self.outname_tofix = outname_tofix

    def process_butches(self):
        scales_obj = Scales()
        agregate_obj = Agregator({})
        write_obj = Writer(self.outname_restored, self.outname_tofix)

        for line in self.query_completion_file:
            pair = line.strip().split(';')
            if not len(pair) == 2:
                continue

            scales_obj.weigh_match(pair)
            if scales_obj.light_match:

                # сбрасывает фрагмент обработанного массива в файлы
                if self.n % self.memory_limit == 0:
                    agregate_obj.agregate_matches(scales_obj.light_match)
                    write_obj.write_matches(agregate_obj.restored, agregate_obj.tofix_manually)

                    agregate_obj = Agregator(self.last_known)

                else:
                    agregate_obj.agregate_matches(scales_obj.light_match)
                    # если конец фрагмемнта близок, запоминает последние 3 пары
                    if self.n % self.memory_limit >= self.memory_limit - 3:
                        self.last_known[scales_obj.light_match.query] = (scales_obj.light_match.weight,
                                                                         scales_obj.light_match.init_str,
                                                                         scales_obj.light_match.complete)
            self.n += 1
            # делает отчет
            if self.n % self.reporting == 0:
                print(self.n, 'lines processed')
        write_obj.write_matches(agregate_obj.restored, agregate_obj.tofix_manually)
