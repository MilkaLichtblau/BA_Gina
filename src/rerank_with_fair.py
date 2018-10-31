import fair.post_processing_methods.fair_ranker.create as fair
import format as fw
import globals as glob
import pandas as pd

from fair.dataset_creator.candidate import Candidate


def rerank_features(filename, dest_file, columnsToWrite, header=None, format=True):
    file = open(filename, 'r')
    data = pd.read_csv(file, usecols=columnsToWrite, sep=",")
    reranked_features = pd.DataFrame()

    # re-rank with fair for every query
    for query in data[glob.query].unique():
        print("Rerank for query " + str(query))
        data_query = data.query(glob.query + "==" + str(query))

        protected, nonProtected = create(data_query)

        p = len(data_query.query(glob.protected_attribute + "==1")) / len(data_query)
        fairRanking, fairNotSelected = fair.fairRanking(glob.amount_candidates, protected, nonProtected, p, glob.alpha)
        fairRanking = setNewQualifications(fairRanking)

        # swap original qualification with fair qualification
        for candidate in fairRanking:
            candidate_row = pd.DataFrame(data_query.query(glob.judgement + "==" + str(candidate.originalQualification)))
            candidate_row.iloc[0, data_query.columns.get_loc(glob.judgement)] = candidate.qualification

            reranked_features = reranked_features.append(candidate_row.iloc[0])

    # sort by judgement to ease evaluation of output
    reranked_features_sorted = pd.DataFrame()
    for query in data[glob.query].unique():
        sorted = reranked_features.query(glob.query + "==" + str(query)).sort_values(by=glob.judgement, ascending=False)
        reranked_features_sorted = reranked_features_sorted.append(sorted)

    # set relevance label
    if glob.relevance_label_range:
        relevance_labels(reranked_features_sorted, glob.relevance_label_range)

    reranked_features_sorted = reranked_features_sorted[columnsToWrite]
    fw.format_and_write(reranked_features_sorted, dest_file, columnsToWrite, header=header, format=format, rerank=True)


def create(data):
    protected = []
    nonProtected = []
    for row in data.itertuples():
        # change to different index in row[.] to access other columns from csv file
        if row[data.columns.get_loc(glob.protected_attribute) + 1] == 0.:
            nonProtected.append(Candidate(row[data.columns.get_loc(glob.judgement) + 1], []))
        else:
            protected.append(Candidate(row[data.columns.get_loc(glob.judgement) + 1], glob.protected_group))

    # sort candidates by judgment in TREC data
    protected.sort(key=lambda candidate: candidate.qualification, reverse=True)
    nonProtected.sort(key=lambda candidate: candidate.qualification, reverse=True)

    return protected, nonProtected


def setNewQualifications(fairRanking):
    qualification = len(fairRanking)
    for candidate in fairRanking:
        candidate.qualification = qualification
        qualification -= 1
    return fairRanking


def relevance_labels(df, range):
    for index, row in df.iterrows():
        df.loc[index, glob.judgement] = round(df.loc[index, glob.judgement] / (glob.amount_candidates / range)) - 1
        if df.loc[index, glob.judgement] < 0:
            df.loc[index, glob.judgement] = 0


