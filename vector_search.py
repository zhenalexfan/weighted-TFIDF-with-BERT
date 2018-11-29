import faiss
from faiss import normalize_L2
import joblib
import numpy as np

verbose = False # set it to True when debugging 

FILE_VEC = 'data/res.pkl'
FILE_SUBSENTENCE = 'data/extend_mask_input.txt'
FILE_ALL_SENTENCE = 'data/All Sentences.txt'

def load_data():
	global vec
	global substcs
	global sentences
	print('Loading sentences and vectors. This may take a few minutes... ')
	with open(FILE_VEC, 'rb') as f:
		vec = joblib.load(f)
	substcs = []
	with open(FILE_SUBSENTENCE, 'r') as f:
	    substcs_ = f.readlines()
	for s in substcs_:
		substcs.append(s.split('\t'))
	with open(FILE_ALL_SENTENCE, 'r') as f:
		sentences = f.readlines()
	# print(np.shape(vec))
	print('Loading data done. ')


def index_data():
	global index
	print('Indexing data... ')
	d = len(vec[0])
	index = faiss.IndexFlatIP(d)
	# print(index.is_trained)
	n_vec = np.array(vec)
	normalize_L2(n_vec)
	index.add(n_vec)
	print('Indexing data done. ')


def search(queries, num_results):
	"""Search top `num_results` similar sentences in `All_sentences.txt` using query vectors `queries`. 
	
	Args:
	    queries (list): a list of query vectors, each row representing a vector
	    num_results (int): the number of results to return
	
	Returns:
	    list, list: a list of list of sentence indices, each row representing a bunch of search results for 
	    a corresponding query vector in `queries` ordered by similarity descendingly, and its corresponding
	    similarity values 
	"""
	if index is None:
		print('Index is None, please index data before searching. ')
		return
	print('Searching %d similar items for %d queries...'
		% (num_results, len(queries)))
	n_queries = np.array(queries, dtype='float32')
	normalize_L2(n_queries)
	D, I = index.search(n_queries, num_results)
	result_sentences = [0 for _ in range(len(queries))]
	result_similarities = [0 for _ in range(len(queries))]
	for query in range(len(queries)):
		if verbose:
			print('No. %d query: ' % query)
		st_similarity_map = {}
		for i, item_idx in enumerate(I[query]):
			sentence_idx, item = substcs[item_idx]
			s = st_similarity_map[sentence_idx] if sentence_idx in st_similarity_map.keys() else 0
			st_similarity_map[sentence_idx] = max(D[query][i], s)
			if verbose: 
				print('  ' + item)
		sorted_stc = sorted(st_similarity_map.items(), key=lambda kv: kv[1], reverse=True)
		result_sentences[query] = [sorted_stc[i][0] for i in range(len(sorted_stc))]
		result_similarities[query] = [sorted_stc[i][1] for i in range(len(sorted_stc))]
	return result_sentences, result_similarities


load_data()
index_data()
if __name__ == '__main__':
	verbose = True
	print('vec 1:', substcs[1])
	print('vec 2:', substcs[2])
	result_indices, result_similarities = search(vec[[1, 2]], 4)
	print(result_indices)
	print(result_similarities)

