import globals as glob


def format_and_write(features, filename, columnsToWrite, format=False, header=None, rerank=False):

    if format:
        id = 1
        for column in features.columns.values:
            if column == glob.judgement:
                set_format(features, column)
            elif column == glob.document:
                format_candidates(features)
            elif column == glob.query:
                set_format_with_colon(features, "qid", column, format_str='%g')
            elif column in columnsToWrite:
                set_format_with_colon(features, id, column)
                id += 1

        features_file = open(filename, 'w')
        features.to_csv(features_file, sep=' ', index=False, header=header, columns=columnsToWrite)

    else:
        features_file = open(filename, 'w')
        features.to_csv(features_file, sep=',', index=False, header=header, float_format='%.5f', columns=columnsToWrite)
    print("Formatted and wrote new feature file: " + filename)


def format_candidates(df):
    for index, row in df.iterrows():
        df.loc[index, glob.document] = "#" + df.loc[index, glob.document]


def set_format_with_colon(df, feature_index, column, format_str='%.5f'):
    for index_format, row_format in df.iterrows():
        try:
            df.loc[index_format, column] = str(feature_index) + ":" + format_str%(df.loc[index_format, column])
        except:
            df.loc[index_format, column] = str(feature_index) + ":" + str(df.loc[index_format, column])


def set_format(df, column, format_str='%g'):
    for index_format, row_format in df.iterrows():
        df.loc[index_format, column] = format_str%(df.loc[index_format, column])


def get_file_name(reranked=False, appendix="", ranker=""):

    file_name = glob.dir + 'features'

    if ranker:
        file_name += "_" + ranker

    if reranked:
        file_name += '_RERANKED'

    file_name += appendix + '.csv'

    return file_name

