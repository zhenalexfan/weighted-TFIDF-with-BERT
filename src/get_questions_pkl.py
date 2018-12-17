import faiss
import joblib
import pickle
import numpy as np

FILE_VEC = '../data/res.pkl'
FILE_SUBSENTENCE = '../data/extend_mask_input (1).txt'
FILE_ALL_SENTENCE = '../data/All Sentences.txt'

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
	print(np.shape(vec))
	print('Loading data done. ')


load_data()
stc_substc_map = {}
for i, substc in enumerate(substcs):
	key_sentence = int(substc[0])
	if key_sentence not in stc_substc_map.keys():
		stc_substc_map[key_sentence] = []
	stc_substc_map[key_sentence].append(i)

print(list(stc_substc_map.items())[: 10])

import mysql.connector
import math

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWD = '12345678'
MYSQL_DB = 'cs510'

cnx = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, database=MYSQL_DB)
cursor = cnx.cursor()
cursor.execute('SELECT Id, Sentences FROM sentences WHERE Id <= 100000 AND Subject_id=0')
questions = cursor.fetchall()
substc_all_questions_indices = []
for q in questions:
	idx_in_all_sentences = q[0] - 1
	substc_all_questions_indices.extend(stc_substc_map[idx_in_all_sentences])
# now substc_all_questions_indices contains all the indices for questions
# corresponding to data/extend_mask_input.txt and res.pkl

header = 'This file includes indices for questions in `res.pkl` or `extend_mask_input (1).txt`'
np.savetxt('data/questions_indices.txt', substc_all_questions_indices, header=header, fmt='%d')
with open('data/questions_vec.pkl', 'wb') as f:
	pickle.dump(vec[substc_all_questions_indices], f)
