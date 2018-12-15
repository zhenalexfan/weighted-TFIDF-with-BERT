import mysql.connector
import math

verbose = False # set it to True when debugging

dataset = "original"
# dataset = "SQuAD"

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWD = '12345678'
MYSQL_DB = 'cs510'

cnx = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, database=MYSQL_DB)
cursor = cnx.cursor()
cursor.execute('select count(id) from sentences')
sentence_count = cursor.fetchall()[0][0]
# print('Document size: %d' % sentence_count)
cursor.execute('select word, count from words')
words = cursor.fetchall()
# print('Vocabulory size: %d' % len(words))


idf = {}
for i, word in enumerate(words):
	idf[word[0]] = math.log(2, sentence_count/word[1])
# print(idf)


def get_sentences_including(query_word, duplicate):
	if dataset == "original":
		cursor.execute('select * from words where word="%s"' % query_word)
		row = cursor.fetchall()
		if row is None or len(row) == 0:
			return []
		else:
			row = row[0]
		sentences = row[2].split(' ')
		sentences = [int(i) for i in sentences]
		return sentences if duplicate else list(set(sentences))


def search(query, num_results, bool_tf=False):
	"""Search top `num_results` sentences using string `query` based on TF-IDF model. If `num_results`
	is 0, the function returns all the results.

	Args:
	    query (str): a query input made of words seperated by spaces (' ')
	    num_results (int): the number of results to return. 0 indicating all the results

	Returns:
	    list: a list of sentences indices ordered by relevance descendingly
	"""
	sentence_score_map = {}
	qwords = query.strip().split(' ')
	for qword in qwords:
		qword = qword.lower()
		sentences = get_sentences_including(qword, duplicate=not bool_tf)
		for sentence in sentences:
			if sentence not in sentence_score_map.keys():
				sentence_score_map[sentence] = 0
			sentence_score_map[sentence] += 1 * idf[qword]
	result = sorted(sentence_score_map.items(), key=lambda kv: kv[1], reverse=True)
	if num_results == 0:
		num_results = len(results)
	result_sent_indices = [i[0] for i in result[:num_results]]
	result_sent_scores = [i[1] for i in result[:num_results]]
	return result_sent_indices, result_sent_scores


if __name__ == '__main__':
	verbose = True
	results = search("Go to a search site", 3)
	print(results)
	for i, r in enumerate(results[0]):
		print('\n***** Result %d *****' % i)
		cursor.execute(
			'select sentences from sentences where id = %d' % r)
		ss = cursor.fetchall()
		print([x[0] for x in ss])
		print()
