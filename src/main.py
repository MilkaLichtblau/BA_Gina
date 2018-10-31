import argparse
import rank as rank
import format as fw
import rerank_with_fair as rr
import globals as glob
import merge
import plot
import fairnessMeasures as fm

parser = argparse.ArgumentParser()

parser.add_argument("-rank", help="Ranks the features given the continuous judgements, gives relevance labels according to -rl"
                                         "and formats the features according to RankLib requirements.", action="store_true")
parser.add_argument("-rerank", help="Reranks the features with FA*IR according to arguments -alpha, -protected_attribute and -protected_group", action="store_true")
parser.add_argument("-plot", help="Plots the distribution of the predicted rankings and shows top 50 rankings.", action="store_true")
parser.add_argument("-merge", help="Merges the predicted scores with the initial feature file.", action="store_true")
parser.add_argument("-measure", help="Measures rKL, DIR, DTR and Fairness@k for the predicted scores.", action="store_true")


# global arguments
parser.add_argument("-f", "--file", help="The feature file that is supposed to ranked be ranked. For initial ranking, "
                                         "the format should contain a header and comma as separator.", type=str)
parser.add_argument("-d", "--dir", help="The directory where the output files should be saved. Default is the current directory.", type=str)
parser.add_argument("-fa", "--filename_appendix", help="An appendix that is added to the filename of the feature file. Might be useful to mark files as training sets.", type=str)
parser.add_argument("-q", "--query", help="Name of the query_id column. Default is 'query_id'.", type=str)
parser.add_argument("-j", "--judgement", help="Name of the judgement column. Default is 'judgment'.", type=str)
parser.add_argument("-doc", "--document", help="Name of the document_id column. Default is 'document_id'.", type=str)
parser.add_argument("-pa", "--protected_attribute", help="Name of the protected_attribute. Default is 'gender'.", type=str)
parser.add_argument("-pg", "--protected_group", help="Name of the protected_group column. Default is 'female'.", type=str)
parser.add_argument("-ac", "--amount_candidates", help="Amount of candidates in ranking. Default is 1092.", type=int)
parser.add_argument("-rs", "--range_start", help="Range start of queries to be ranked. Default is 1", type=int)
parser.add_argument("-re", "--range_end", help="Range end of queries to be ranked. Default is 50", type=int)
parser.add_argument("-rl", "--relevance_label_range", help="Range of relevance labels. Default is 5, meaning a range from 0-4", type=int)
parser.add_argument("-a", "--alpha", help="Alpha adjustment for FA*IR algorithm. Default is 0.1", type=float)
parser.add_argument("-ctw", "--columnsToWrite", help="Columns to write in feature file with relevance labels. By default all TREC features.")
parser.add_argument("-ctwi", "--columnsToWriteInital", help="Columns to write in feature file with continuous ranks. By default all TREC features.")
parser.add_argument("-pf", "--prediction_file", help="Predicted scores.")
parser.add_argument("-r", "--ranker", help="Used ranker for plot title.")
parser.add_argument("-rr", "--reranked", help="Is reranked for plot title.", action="store_true")
parser.add_argument("-o", "--optimized", help="Is optimized towards some metric for plot title.", type=bool)
parser.add_argument("-k", "--k", help="Length of ranking for fairness measures. Default is 1000", type=int)


args = parser.parse_args()


glob.filename_origin = args.file if args.file else glob.filename_origin
glob.dir = args.dir if args.dir else glob.dir
glob.query = args.query if args.query else glob.query
glob.judgement = args.judgement if args.judgement else glob.judgement
glob.document = args.document if args.document else glob.document
glob.protected_attribute = args.protected_attribute if args.protected_attribute else glob.protected_attribute
glob.protected_group = args.protected_group if args.protected_group else glob.protected_group
glob.amount_candidates = args.amount_candidates if args.amount_candidates else glob.amount_candidates
glob.range_start = args.range_start if args.range_start else glob.range_start
glob.range_end = args.range_end if args.range_end else glob.range_end
glob.relevance_label_range = args.relevance_label_range if args.relevance_label_range else glob.relevance_label_range
glob.alpha = args.alpha if args.alpha else glob.alpha
glob.columnsToWrite = args.columnsToWrite if args.columnsToWrite else glob.columnsToWrite
glob.columnsToWriteInital = args.columnsToWriteInital if args.columnsToWriteInital else glob.columnsToWriteInital
glob.k = args.k if args.k else glob.k

appendix = args.filename_appendix if args.filename_appendix else ""
ranker = args.ranker
reranked = args.reranked if args.reranked else False
optimized = args.optimized

if args.rank and args.rerank:
    # initial ranking with header for reranking
    features_ranked_with_header = fw.get_file_name(ranker="ContinuousRanking", appendix=appendix)
    file = open(glob.filename_origin, 'r')
    rank.rank_features(file, features_ranked_with_header, glob.columnsToWriteInital, header=True, format=False)

    # ranking with format
    features_ranked = fw.get_file_name(appendix=appendix)
    file = open(glob.filename_origin, 'r')
    rank.rank_features(file, features_ranked, glob.columnsToWrite)

    # reranking with format
    features_reranked = fw.get_file_name(reranked=True, appendix=appendix)
    rr.rerank_features(features_ranked_with_header, features_reranked, glob.columnsToWrite)
elif args.rank:
    # initial ranking with header for reranking
    features_ranked_with_header = fw.get_file_name(ranker="ContinuousRanking", appendix=appendix)
    file = open(glob.filename_origin, 'r')
    rank.rank_features(file, features_ranked_with_header, glob.columnsToWriteInital, header=True, format=False)

    # ranking with format
    features_ranked = fw.get_file_name(appendix=appendix)
    file = open(glob.filename_origin, 'r')
    rank.rank_features(file, features_ranked, glob.columnsToWrite)
elif args.rerank:
    # initial ranking with header for reranking
    features_ranked_with_header = fw.get_file_name(ranker="ContinuousRanking", appendix=appendix)
    file = open(glob.filename_origin, 'r')
    rank.rank_features(file, features_ranked_with_header, glob.columnsToWriteInital, header=True, format=False)

    # reranking with format
    features_reranked = fw.get_file_name(reranked=True, appendix=appendix)
    rr.rerank_features(features_ranked_with_header, features_reranked, glob.columnsToWrite)

if args.merge:
    merge.merge(args.prediction_file, args.file)

if args.plot:
    plot.plot(glob.filename_origin, ranker, reranked, optimized=optimized)

if args.measure:
    fm.measureFairness(glob.filename_origin, ranker, reranked, args.k, glob.dir)