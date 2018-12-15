import numpy as np

# 这个例子用来说明两个search怎么用. 
# 在此之前, 去tfidf_search.py和vector_search.py分别代码中的常量（数据库
# 配置、句子向量文件的位置等）是否正确. 

# 利用TF-IDF搜索
# 利用TF-IDF搜索输入一个字串, 搜索出来的index是文档的index, 也就是对应sentences
# 这个表里面的QA_idx字段的数据. 
print('TF-IDF Model Search')
import tfidf_search
results = tfidf_search.search("Go to a search site", 3, bool_tf=False)
print(results[0], end='\n===\n')

for i, r in enumerate(results[0]):
	print('***** Result %d *****' % i)
	tfidf_search.cursor.execute(
		'select sentences from sentences where id = %d' % r)
	ss = tfidf_search.cursor.fetchall()
	print('\n'.join([x[0] for x in ss]))
	print()


# how 6696 6702 6713 6720