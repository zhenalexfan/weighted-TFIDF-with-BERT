import query_type_client
import tfidf_search
import bert_sim_search

query = input()
query_type = query_type_client.get_query_type(query)
if query_type == query_type_client.QUERY_TYPE_WORDS:
    sents, scores = tfidf_search.search(query, 10)
    print(sents, scores)
elif query_type == query_type_client.QUERY_TYPE_SENTENCE:
    p_sents, p_scores = tfidf_search.search(query, 100)
    # sents, sims = bert_sim_search.search_in_range(query, 10, data_subset=p_sents)
    # print(sents, sims)
