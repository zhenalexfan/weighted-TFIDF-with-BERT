import json
import string
import numpy as np
import spacy
import re
from termcolor import colored


SENTENCE_MIN_LEN = 10
SENTENCE_MAX_LEN = 128

# load data
data = []
with open('data/train-v2.0.json') as f:
	data = json.load(f)['data']

# tokenizer for splitting sentences
# tokenizer = nltk.data.load('/Users/alexfanchina/nltk_data/tokenizers/punkt/english.pickle')
nlp = spacy.load('en')

# use data
sentences = []
labels = []

def tag_tokens_from_to(doc, array, lo, hi):
	assert len(doc) == len(array)
	for i, token in enumerate(doc):
		if token.idx >= lo and token.idx < hi:
			array[i] = 1

def print_colored_sentence(sent, label):
	sent_ = sent.as_doc()
	for token in sent_:
		if label[token.i] == 0:
			print(token.text_with_ws, end='')
		else:
			print(colored(token.text_with_ws, 'red'), end='')
	print()


for idx, datum in enumerate(data[:]):
	paras = datum['paragraphs']
	for p in paras:
		context = p['context']
		context_doc = nlp(context)
		res = [0 for _ in context_doc]
		qas = p['qas']
		for qa in qas:
			answers = qa['answers']
			for ans in answers:
				ans_text = ans['text']
				ans_start = int(ans['answer_start'])
				ans_end = ans_start + len(ans_text)
				tag_tokens_from_to(context_doc, res, ans_start, ans_end)
				# print(ans_text)
		for sent in context_doc.sents:
			if '\n' in sent.text or len(sent) < SENTENCE_MIN_LEN or len(sent) >= SENTENCE_MAX_LEN:
				continue
			label = res[sent.start : sent.end]
			if 1 not in label:
				continue
			assert len(label) == len(sent)
			sentences.append(sent.text)
			labels.append(label)
			# print_colored_sentence(sent, label)
		# print()
	print('Finish %d in %d' % (idx, len(data)))


def save_sentences(filename, sentences_):
	print('Writing %d sentences to %s...' % (len(sentences_), filename))
	with open('data/SQuAD/%s.txt' % filename, 'w', encoding='utf-8') as f:
		for item in sentences_:
			f.write(item + '\n')

def save_labels(filename, labels_):
	print('Writing %d sequences to %s...' % (len(labels_), filename))
	with open('data/SQuAD/%s.txt' % filename, 'w') as f:
		for l in labels_:
			f.write(' '.join(str(x) for x in l) + '\n')


save_sentences('sentences-remove-zeros', sentences)
save_labels('labels-remove-zeros', labels)

# sentences = np.array(sentences)
# labels = np.array(labels)
# train_size = int(len(sentences) * 0.7)
# dev_size = int(len(sentences) * 0.2)
# test_size = int(len(sentences) * 0.1)
# train_indices = np.random.choice(list(range(len(sentences))), train_size, replace=False)
# dev_and_test_indices = list(set(range(len(sentences))) - set(train_indices))
# dev_indices = np.random.choice(dev_and_test_indices, dev_size, replace=False)
# test_indices = list(set(dev_and_test_indices) - set(dev_indices))

# save_sentences('train-sentences', sentences[train_indices])
# save_labels('train-labels', labels[train_indices])
# save_sentences('dev-sentences', sentences[dev_indices])
# save_labels('dev-labels', labels[dev_indices])
# save_sentences('test-sentences', sentences[test_indices])
# save_labels('test-labels', labels[test_indices])
