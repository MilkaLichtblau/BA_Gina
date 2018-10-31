import globals as glob
import pandas as pd
import numpy as np
from measures.candidateCreator.createCandidate import createCandidate as cC
from measures.runMetrics import runMetrics


def measureFairness(filename, ranker, reranked, k, dir, optimized=None):
    ranking, queryNumbers = cC.createLearningCandidate(filename)
    unprotected = []
    protected = []

    protected = list(filter(lambda x: x.isProtected, ranking))
    unprotected = list(filter(lambda x: not x.isProtected, ranking))

    dataset = "RANKED"
    if reranked:
        dataset = "RERANKED"
    results = runMetrics(k, protected, unprotected, ranking, ranking, dataset, ranker)

    df = pd.DataFrame(np.array(results).reshape(len(results), 4),
                      columns=['Data_Set_Name', 'Algorithm_Name', 'Measure', 'Value'])

    df.to_csv(dir + "/" + dataset + ".csv", index=(False))

