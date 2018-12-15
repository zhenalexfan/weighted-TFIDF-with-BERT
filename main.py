import query_type_client
import tfidf_search

query = input()
query_type = query_type_client.get_query_type(query)
if query_type == query_type_client.QUERY_TYPE_WORDS:
    print(tfidf_search.search(query, 10))
elif query_type == query_type_client.QUERY_TYPE_SENTENCE:
    print(tfidf_search.search(query, 100))
    # use bert server for vector
    # vector search in the returned sentences
