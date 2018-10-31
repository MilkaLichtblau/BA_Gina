import pandas as pd
import globals as glob


def merge(prediction_filename, features_file):
    prediction_header = [glob.query, "q0", glob.document, "rank", "score", "indri"]
    prediction_file = open(prediction_filename, "r")
    prediction = pd.read_csv(prediction_file, sep=" ", names=prediction_header)

    features_header = glob.columnsToWrite
    features = pd.read_csv(features_file, sep=" ", names=features_header)

    features[glob.query] = features[glob.query].map(lambda x: int(x.lstrip("qid:")))
    features[glob.protected_attribute] = features[glob.protected_attribute].map(lambda x: float(x[2:]))
    features[glob.document] = features[glob.document].map(lambda x: x[1:])

    features = features.merge(prediction, left_on=[glob.query, glob.document], right_on=[glob.query, glob.document], how='inner')

    final = pd.DataFrame()
    for i in features[glob.query].unique():
        query = features.query(glob.query + "==" + str(i))
        query = query.sort_values(by=["rank"])
        final = final.append(query)
    final.to_csv(prediction_filename[:-4] + "_MERGED.csv", sep=",", index=False, header=True)