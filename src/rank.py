import pandas as pd
import format as fw
import globals as glob


def rank_relevant_group(group, score, step_size, amount_candidates, amount_candidates_max):
    for index, row in group.iterrows():
        if amount_candidates <= amount_candidates_max:
            group.loc[index, glob.judgement] = score
            group.update(group[glob.judgement].astype('float64'))
            score -= step_size
            amount_candidates += 1
    group = group.query(glob.judgement + "!=0.0")
    return group, score, amount_candidates


def rank_non_relevant_group(group, score, step_size, amount_candidates, amount_candidates_max, non_experts_amount_max):
    non_relevant_amount_max_count = 0
    for index, row in group.iterrows():
        if amount_candidates <= amount_candidates_max:
            if non_relevant_amount_max_count <= non_experts_amount_max:
                group.loc[index, glob.judgement] = score
                group.update(group[glob.judgement].astype('float64'))
                score -= step_size
                non_relevant_amount_max_count += 1
                amount_candidates += 1
            else:
                break
    group = group.query(glob.judgement + "!=0.0")
    return group, score, amount_candidates


def rank_features(file, dest_file, columnsToWrite, header=None, format=True):

    # importing the data from csv and drop of the document_id column
    data_csv = pd.read_csv(file, delimiter=',')

    # new file with rankings
    features_df = pd.DataFrame()

    for i in range(glob.range_start, glob.range_end + 1):
        print("Ranking for query " + str(i))

        query_features = data_csv.query(glob.query + "==" + str(i))

        # collecting the 4 groups (protected/non-protected, relevant/non-relevant)
        protected_relevant = query_features.query(glob.protected_attribute + "==1").query(glob.judgement + "==1")
        protected_relevant_amount = len(protected_relevant)

        protected_non_relevant = query_features.query(glob.protected_attribute + "==1").query(glob.judgement + "==0")
        protected_non_relevant_amount = len(protected_non_relevant)

        unprotected_relevant = query_features.query(glob.protected_attribute + "==0").query(glob.judgement + "==1")
        unprotected_relevant_amount = len(unprotected_relevant)

        unprotected_non_relevant = query_features.query(glob.protected_attribute + "==0").query(glob.judgement + "==0")

        # calculating the ratio of protected/non-protected non-relevant
        ratio_protected = (protected_relevant_amount + protected_non_relevant_amount) / len(query_features)
        protected_non_relevant_amount_max = round(ratio_protected * glob.amount_candidates - protected_relevant_amount)
        unprotected_non_relevant_amount_max = glob.amount_candidates - (protected_relevant_amount + unprotected_relevant_amount + protected_non_relevant_amount_max)

        # determining the max-score
        score = glob.amount_candidates
        step_size = score/glob.amount_candidates

        # score the four groups
        amount_candidates = 0

        unprotected_relevant, score, amount_candidates = rank_relevant_group(unprotected_relevant, score, step_size, amount_candidates, glob.amount_candidates)
        protected_relevant, score, amount_candidates = rank_relevant_group(protected_relevant, score, step_size, amount_candidates, glob.amount_candidates)
        unprotected_non_relevant, score, amount_candidates = rank_non_relevant_group(unprotected_non_relevant, score, step_size,
                                                                                     amount_candidates, glob.amount_candidates, unprotected_non_relevant_amount_max)
        protected_non_relevant, score, amount_candidates = rank_non_relevant_group(protected_non_relevant, score, step_size, amount_candidates,
                                                                                   glob.amount_candidates, protected_non_relevant_amount_max)

        # concat the 4 groups to one data frame
        features_df = pd.concat([features_df, unprotected_relevant, protected_relevant, unprotected_non_relevant, protected_non_relevant])

    if format and glob.relevance_label_range:
        relevance_labels(features_df, glob.relevance_label_range)

    # format and write the new data frame with scores
    print("Writing " + dest_file + " to file.")
    fw.format_and_write(features_df, dest_file, columnsToWrite, format=format, header=header)


def relevance_labels(df, range):
    for index, row in df.iterrows():
        df.loc[index, glob.judgement] = round(df.loc[index, glob.judgement] / (glob.amount_candidates / range)) - 1
        if df.loc[index, glob.judgement] < 0:
            df.loc[index, glob.judgement] = 0