'''
Global variables for feature ranking and formatting
'''

filename_origin = '../data/features.csv'
dir = '../data/formatted_data/'

query = "query_id"
judgement = "judgment"
document = "document_id"
rank = "rank"

protected_attribute = "gender"
protected_group = "female"

amount_candidates = 1092 #1092
range_start = 1
range_end = 50
range_start_rerank = 51
range_end_rerank = 60

relevance_label_range = 5

# alpha for FA*IR algorithm
alpha = 0.1

k = 1000

columnsToWriteInital = ["query_id", "document_id", "gender", "match_body_email_subject_score_norm",
                  "match_body_email_subject_term_count", "match_body_email_subject_df_min",
                  "match_body_email_subject_df_max", "match_body_email_subject_df_stdev",
                  "match_body_email_subject_df_sum", "match_body_email_subject_idf_min",
                  "match_body_email_subject_idf_max", "match_body_email_subject_idf_stdev",
                  "match_body_email_subject_idf_sum", "match_body_email_subject_tf_min",
                  "match_body_email_subject_tf_max", "match_body_email_subject_tf_stdev",
                  "match_body_email_subject_tf_sum", "match_body_term_count", "match_body_score_norm",
                  "match_subject_score_norm", "match_subject_term_count", "judgment", "mail_count"]

columnsToWrite = ["judgment", "query_id", "gender", "match_body_email_subject_score_norm",
                  "match_body_email_subject_term_count", "match_body_email_subject_df_min",
                  "match_body_email_subject_df_max", "match_body_email_subject_df_stdev",
                  "match_body_email_subject_df_sum", "match_body_email_subject_idf_min",
                  "match_body_email_subject_idf_max", "match_body_email_subject_idf_stdev",
                  "match_body_email_subject_idf_sum", "match_body_email_subject_tf_min",
                  "match_body_email_subject_tf_max", "match_body_email_subject_tf_stdev",
                  "match_body_email_subject_tf_sum", "match_body_term_count", "match_body_score_norm",
                  "match_subject_score_norm", "match_subject_term_count","document_id"]