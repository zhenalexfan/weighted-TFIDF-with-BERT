import mysql.connector
import math

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWD = '12345678'
MYSQL_DB = 'cs510'

cnx = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, database=MYSQL_DB)
cursor = cnx.cursor()
cursor.execute('select max(QA_id) from sentences')
doc_count = cursor.fetchall()[0][0]
# print('Document size: %d' % doc_count)
cursor.execute('select word, count from words')
words = cursor.fetchall()
# print('Vocabulory size: %d' % len(words))


idf = {}
for i, word in enumerate(words):
	idf[word[0]] = math.log(2, doc_count/word[1])


def count(qa_id, word):
	print('count(%d, %s)' % (qa_id, word))
	cursor.execute('select sentences from sentences where QA_id=%d' % qa_id)
	sentences = cursor.fetchall()
	count = 0
	total = 0
	# print(sentences)
	for sentence in sentences:
		count += sentence[0].lower().count(word)
		total += len(sentence[0].split(' '))
	return count/total


def search(query, num_results):
	"""Search top `num_results` documents using string `query` based on TF-IDF model. If `num_results` 
	is 0, the function returns all the results. 
	
	Args:
	    query (str): a query input made of words seperated by spaces (' ')
	    num_results (int): the number of results to return. 0 indicating all the results
	
	Returns:
	    list: a list of documents indices ordered by relevance descendingly
	"""
	doc_score_map = {}
	qwords = query.strip().split(' ')
	for qword in qwords:
		cursor.execute('select * from words where word="%s"' % qword)
		row = cursor.fetchall()
		if row is None or len(row) == 0:
			continue
		else:
			row = row[0]
		docs = row[2].split(' ')
		for doc in docs:
			doc = int(doc)
			if doc not in doc_score_map.keys():
				doc_score_map[doc] = 0
			doc_score_map[doc] += 1 * idf[qword]
	result = sorted(doc_score_map.items(), key=lambda kv: kv[1], reverse=True)
	return [i[0] for i in result[:num_results]] if num_results > 0 else [i[0] for i in result]


if __name__ == '__main__':
	print(search('what the fuck', 10))
