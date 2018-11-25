import faiss
import joblib
import numpy as np

FILE_VEC = 'data/sentVec.pkl'
FILE_SUBSENTENCE = 'data/extend_mask_input.txt'
FILE_ALL_SENTENCE = 'data/All Sentences.txt'

def load_data():
	global vec
	global substcs
	global sentences
	with open(FILE_VEC, 'rb') as f:
		vec_ = joblib.load(f)
	vec = np.array(vec_)[:, 0, :]
	substcs = []
	with open(FILE_SUBSENTENCE, 'r') as f:
	    substcs_ = f.readlines()
	for s in substcs_:
		substcs.append(s.split('\t'))
	with open(FILE_ALL_SENTENCE, 'r') as f:
		sentences = f.readlines()
	# print(np.shape(vec))

def index_data():
	d = len(vec[0])
	index = faiss.IndexFlatL2(d)
	# print(index.is_trained)
	index.add(np.ascontiguousarray(vec))
	return index

def search(index, queries, k):
	print('Searching %d similar items for %d queries...'
		% (k, len(queries)))
	D, I = index.search(np.ascontiguousarray(queries), k)
	result = [0 for _ in range(len(queries))]
	for query in range(len(queries)):
		print('No. %d query: ' % query)
		st_similarity_map = {}
		for i, item_idx in enumerate(I[query]):
			sentence_idx, item = substcs[item_idx]
			s = st_similarity_map[sentence_idx] if sentence_idx in st_similarity_map.keys() else 0
			st_similarity_map[sentence_idx] = max(D[query][i], s)
			print('  ' + item)
		sorted_stc = sorted(st_similarity_map.items(), key=lambda kv: kv[1])
		result[query] = [sorted_stc[i][0] for i in range(len(sorted_stc))]
	return result


load_data()
index = index_data()
if __name__ == '__main__':
	print(search(index, vec[[1, 2]], 4))
