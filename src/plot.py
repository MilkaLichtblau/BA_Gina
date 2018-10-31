import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib as mpl

import globals as glob

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)
    s = s.split('.')[0]
    # The percent symbol needs escaping in latex
    if mpl.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'

def plot(filename, ranker, reranked, optimized=None):
    """
    Distribution Plot
    """

    plt.rcParams.update({'font.size': 20, 'lines.linewidth': 3, 'lines.markersize': 15, 'font.family': 'DejaVu Sans'})
    plt.rcParams['ps.useafm'] = True
    plt.rcParams['pdf.use14corefonts'] = True
    plt.rcParams['text.usetex'] = True

    # plt_title = ranker
    # if optimized:
    #     plt_title += " (" + optimized + ")"
    # plt_title += "\n"
    # if reranked:
    #     plt_title += "Average rankings of test data based on model with re-rankings"
    # else:
    #     plt_title += "Average rankings of test data based on model with initial rankings"

    df = pd.read_csv(open(filename, 'r'), sep=",")

    fig = plt.figure(figsize=(18, 12))

    male = df.query(glob.protected_attribute + "==0.0")["rank"]

    female = df.query(glob.protected_attribute + "==1.0")["rank"]
    legend = ['Non-protected', 'Protected']

    bins = np.linspace(0, 1092, 1092/25)
    male_hist = np.histogram(male, bins=bins, range=(0, 1092))
    female_hist = np.histogram(female, bins=bins, range=(0, 1092))

    male_rate_rel = male_hist[0] / (male_hist[0] + female_hist[0])
    female_rate_rel = female_hist[0] / (male_hist[0] + female_hist[0])

    plt.bar(bins[:-1], female_rate_rel, width=0.8*(bins[1] - bins[0])/2, color="green")
    plt.bar(bins[:-1]+ (bins[1] - bins[0])/2, male_rate_rel, width=0.95*(bins[1] - bins[0])/2, color="orange")


    plt.xlabel("Positions in the ranking")
    plt.ylabel("Ratio of protected candidates over the ranking positions")

    plt.xticks(np.arange(0,1093, step=100))
    plt.yticks(np.arange(0, 1.1, step=0.1))

    formatter = FuncFormatter(to_percent)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.axis([0, 1093, 0, 1])
    plt.margins(0)
    plt.legend(legend)

    #plt.title(plt_title)
    #plt.show()
    fig.savefig(filename[:-4] + '.png', bbox_inches='tight', dpi=300)

    """



    # Top 50 Plot
    # """
    df = pd.read_csv(filename)

    # plt_title = ranker
    # if optimized:
    #     plt_title += "(" + optimized + ")"
    # plt_title += "\n"
    # if reranked:
    #     plt_title += "Top 50 ranking positions for rankings of test data based on model with re-rankings"
    # else:
    #     plt_title += "Top 50 ranking positions for rankings of test data based on model with initial rankings"

    fig = plt.figure(figsize=(21, 4))
    for i in df[glob.query].unique():
        x_male = df.query(glob.query + "==" + str(i)).query("rank<" + str(glob.range_start_rerank)).query(glob.protected_attribute + "==0")["rank"]
        x_female = df.query(glob.query + "==" + str(i)).query("rank<" + str(glob.range_start_rerank)).query(glob.protected_attribute + "==1")["rank"]
        y_male = df.query(glob.query + "==" + str(i)).query("rank<" + str(glob.range_start_rerank)).query(glob.protected_attribute + "==0")[
            glob.query]
        y_female = df.query(glob.query + "==" + str(i)).query("rank<" + str(glob.range_start_rerank)).query(glob.protected_attribute + "==1")[
            glob.query]

        plt.scatter(x_male, y_male, marker="+", color="orange")
        plt.scatter(x_female, y_female, marker="o", color="green")

    plt.xticks([1] + list(np.arange(5, 52, 5)))
    plt.yticks(df[glob.query].unique())
    plt.xlabel("Positions in the ranking")
    plt.ylabel("Query ID")
    #plt.title(plt_title)
    legend = ['Non-protected', 'Protected']

    plt.legend(legend)
    #plt.show()
    fig.savefig(filename[:-4] + '_TOP_50.png', bbox_inches='tight', dpi=300)
