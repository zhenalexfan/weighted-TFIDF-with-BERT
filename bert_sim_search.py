import faiss
from faiss import normalize_L2
import joblib
import numpy as np
import logging
from bert_serving.client import BertClient

bc = BertClient()

FILE_VECS = 'data/SQuAD/sentenceVec.pkl'
FILE_SENTENCE = 'data/SQuAD/sentences-remove-zeros.txt'


def load_data():
    global vecs
    global sents
    print('Loading sentences and vectors. This may take a few minutes... ')
    with open(FILE_VECS, 'rb') as f:
        vecs = joblib.load(f)
    with open(FILE_SENTENCE, 'r', encoding='utf8') as f:
        sents = f.readlines()
    logging.debug('vecs shape: %s' % str(np.shape(vecs)))
    print('Loading data done. ')


def index_data():
    global index
    print('Indexing data... ')
    d = len(vecs[0])
    index = faiss.IndexFlatIP(d)
    # print(index.is_trained)
    n_vecs = np.array(vecs)
    normalize_L2(n_vecs)
    index.add(n_vecs)
    print('Indexing data done. ')


def search_with_vectors(q_vectors, num_results):
    """Search top `num_results` similar sentences in `All_sentences.txt` using query vectors `q_vectors`.

    Args:
        q_vectors (list): a list of query vectors, each row representing a vector
        num_results (int): the number of results to return

    Returns:
        list, list: a list of list of sentence indices, each row representing a bunch of search results for
        a corresponding query vector in `q_vectors` ordered by similarity descendingly, and its corresponding
        similarity values
    """
    if index is None:
        index_data()
    logging.debug('Searching %d similar items for %d q_vectors...'
        % (num_results, len(q_vectors)))
    n_queries = np.array(q_vectors, dtype='float32')
    normalize_L2(n_queries)
    result_similarities, result_sentences = index.search(n_queries, num_results)
    return result_sentences, result_similarities


def get_bert_vec(query):
    return bc.encode([query])[0]


def search(query, num_results):
    q_vec = get_bert_vec(query)
    r_sents, r_sims = search_with_vectors([q_vec], num_results)
    return r_sents[0], r_sims[0]


load_data()
index_data()
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    r_sents, r_sims = search("She was listed among the most valuable people", 4)
    print(r_sents)
    print(r_sims)
    for i in r_sents:
        print(sents[i].encode('utf-8'))
