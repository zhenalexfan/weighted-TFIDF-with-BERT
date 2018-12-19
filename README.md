# Improved Semantic Search based on Weighted TF-IDF & BERT

- Group members: Yuxiang Li, Yuxin Xiao, Zhen Fan
- Research report: [Improved Semantic Search based on Weighted TF-IDF & BERT](report/final_report.pdf)

## Abstract
We present an improved semantic search approach based on a weighted TF-IDF method and the BERT natural language model. We motivate the choice of a weighted TF-IDF method via an intuition that the questionable spans in a document summarize the document's topics and hence, should be placed greater emphasis when calculating the TF-IDF score. The use of the BERT natural language model is to complement the weakness of the TF-IDF framework in understanding the true semantic meaning of a document. Therefore, our model encodes a document's questionable spans and true semantics. It scales effectively in the size of the dataset. In a number of semantic search experiments on question-answering datasets, we demonstrate that our approach outperforms traditional models by a significant margin.

## Running the Project
0. Get the [dataset](https://drive.google.com/drive/folders/18BvtoDEc_bm2qa11K6930FbqAYwUqoYp?usp=sharing) into `data/` folder;
1. Import `data/cs510project_new_words.sql` and `data/cs510project_new_sentences.sql` in a MySQL database;
2. Change the MySQL username and passwords in `tfidf_search.py`;
3. Start `query_type_server.py`;
4. Start bert-as-service on localhost. See [hanxiao/bert-as-service](https://github.com/hanxiao/bert-as-service) for details. We use the BERT-Base Uncased model (12-layer, 768-hidden, 12-heads, 110M parameters) for BERT vectors;
5. Run `main.py` and start searching.

## About the course (Fall 2018)
- [Course page](http://times.cs.uiuc.edu/course/510f18/)
- Instructor: [ChengXiang Zhai](http://czhai.cs.illinois.edu/)
- Location: 0216 Siebel Center (SC), UIUC
