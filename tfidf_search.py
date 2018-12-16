import mysql.connector
import math
import logging

# dataset = "original"
dataset = "SQuAD"

if dataset == "original":
	MYSQL_HOST = 'localhost'
	MYSQL_USER = 'root'
	MYSQL_PASSWD = '12345678'
	MYSQL_DB = 'cs510'
	MYSQL_SENTS_TABLE = 'sentences'
	MYSQL_WORDS_TABLE = 'words'
elif dataset == "SQuAD":
	MYSQL_HOST = 'localhost'
	MYSQL_USER = 'root'
	MYSQL_PASSWD = '12345678'
	MYSQL_DB = 'squad_inv_index'
	MYSQL_SENTS_TABLE = 'new_sentences'
	MYSQL_WORDS_TABLE = 'new_words'

cnx = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, database=MYSQL_DB)
cursor = cnx.cursor()
cursor.execute('select count(*) from %s' % MYSQL_SENTS_TABLE)
sentence_count = cursor.fetchall()[0][0]
# print('Document size: %d' % sentence_count)
cursor.execute('select word, count from %s' % MYSQL_WORDS_TABLE)
words = cursor.fetchall()
# print('Vocabulory size: %d' % len(words))

def get_tokens_in(query):
	return query.strip().split(' ')
	# TODO: use spacy

def get_sentences_including(query_word, duplicate=True, return_idf=True):
	cursor.execute('select * from %s where word="%s"' % (MYSQL_WORDS_TABLE, query_word))
	row = cursor.fetchall()
	if row is None or len(row) == 0:
		return [], float('nan')
	else:
		row = row[0]
	sentences = row[2].split(' ')
	sentences = [int(i) for i in sentences]
	sentences_unique = list(set(sentences))
	idf = math.log(2, sentence_count/len(sentences_unique))
	if not duplicate:
		sentences = sentences_unique
	if return_idf:
		return sentences, idf
	else:
		return sentences


def search(query, num_results, bool_tf=True):
	"""Search top `num_results` sentences using string `query` based on TF-IDF model. If `num_results`
	is 0, the function returns all the results.

	Args:
	    query (str): a query input made of words seperated by spaces (' ')
	    num_results (int): the number of results to return. 0 indicating all the results

	Returns:
	    list: a list of sentences indices ordered by relevance descendingly
	"""
	sentence_score_map = {}
	qwords = get_tokens_in(query)
	for qword in qwords:
		qword = qword.lower()
		sentences, idf = get_sentences_including(qword, duplicate=not bool_tf, return_idf=True)
		logging.debug("qword: %-10s, \tidf: %.4f, \ttop 5: %s" % (qword, idf, str(sentences[:5])))
		for sentence in sentences:
			if sentence not in sentence_score_map.keys():
				sentence_score_map[sentence] = 0
			sentence_score_map[sentence] += 1 * idf
	result = sorted(sentence_score_map.items(), key=lambda kv: kv[1], reverse=True)
	if num_results == 0:
		num_results = len(results)
	result_sent_indices = [i[0] for i in result[:num_results]]
	result_sent_scores = [i[1] for i in result[:num_results]]
	return result_sent_indices, result_sent_scores


if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	results = search("The competition began on August 2, 1955, when the Soviet Union responded", 3)
	print(results)
	print()
	for i, r in enumerate(results[0]):
		print('***** Result %d *****' % i)
		cursor.execute(
			'select sentence from %s where sentence_id = %d' % (MYSQL_SENTS_TABLE, r))
		ss = cursor.fetchall()
		print([x[0].encode('utf-8') for x in ss])
		print()
