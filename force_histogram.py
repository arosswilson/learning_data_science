# import force_first
import force_connectivity
import thinkstats
import math
from collections import Counter
import matplotlib.pyplot as pyplot

def create_histogram(data_dir='.'):
    table = force_connectivity.Cases()
    table.ReadRecords(data_dir)

    table.pain_counts = [c.registered_pain_count for c in table.records if c.registered_pain_count and c.registered_pain_count > 5]

    table.cis_hist = Counter(table.pain_counts)
    n = len(table.pain_counts)

    print(table.cis_hist.items())
    table.cis_pmf = {x:(freq/n) for x,freq in table.cis_hist.items()}
    return table

def plot_historgram(hist_dict):
    ks, vs = [], []
    for k, v in hist_dict.items():
        ks.append(k)
        vs.append(v)
    print(ks)
    print(vs)
    hist = pyplot.bar(ks, vs)
    pyplot.show()

def main(name, data_dir='.'):
    table=create_histogram(data_dir)
    plot_historgram(table.cis_pmf)

if __name__ == '__main__':
    import sys
    main(*sys.argv)



