import numpy as np

# 这个例子用来说明两个search怎么用. 
# 在此之前, 去tfidf_search.py和vector_search.py分别代码中的常量（数据库
# 配置、句子向量文件的位置等）是否正确. 

# 利用TF-IDF搜索
# 利用TF-IDF搜索输入一个字串, 搜索出句子的index, 也就是sentence表里面的id字段的数据. 
print('TF-IDF Model Search')
import tfidf_search
print(tfidf_search.search('what the fuck', 5), end='\n\n')

# 向量搜索
# 这里可以同时输入一些768维的向量 (下面例子里只输入了一个), 搜索出来的index是相似
# 句子的index, 即extend_mask_input.txt里面子句前的标号, 也是All Sentences.txt
# 中句子的位置. 
print('Similarity Search')
import vector_search  # This import may take several minutes
vecs = np.random.random((1, 768)).astype('float32') # 这里随机生成一个向量来用
print(vector_search.search(vecs, 5))