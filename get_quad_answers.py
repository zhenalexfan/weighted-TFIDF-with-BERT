import json
import string
import numpy as np
import nltk.data
import re

# load data
data = []
with open('data/train-v2.0.json') as f:
	data = json.load(f)['data']

# tokenizer for splitting sentences
tokenizer = nltk.data.load('/Users/alexfanchina/nltk_data/tokenizers/punkt/english.pickle')

# table for removing puntuations
table = str.maketrans({key: None if key != '\'' and key != '-' else key for key in string.punctuation})

# use data
sentences = []
seqs = []

for datum in data:
	paras = datum['paragraphs']
	for p in paras:
		context = p['context']
		cwords = context.split(' ')
		res = [0 for _ in cwords]
		if ('' in cwords): 
			print('space')
		qas = p['qas']
		for qa in qas:
			answers = qa['answers']
			for ans in answers:
				ans_text = ans['text']
				num_before = len(context[:context.find(ans_text)].split(' '))
				num_words = len(ans_text.split(' '))
				# print(ans_text)
				# print(str(cwords[num_before - 1: num_before - 1 + num_words]))
				for i in range(num_before - 1, num_before - 1 + num_words):
					res[i] = 1
		
		stcs = tokenizer.tokenize(context)
		delimiters = [context.find(x) for x in stcs]
		delimiters.append(len(context))
		word_start = 0
		for i in range(len(delimiters) - 1):
			start = delimiters[i]
			end = delimiters[i + 1]
			stc = stcs[i]
			sword = stc.split(' ')
			n = len(sword)
			seq = res[word_start: word_start + n]
			word_start += n

			for i, word in enumerate(sword):
				if word == '':
					del sword[i]
					del seq[i]
			if (len(seq) == 0):
				continue
			sentences.append(' '.join(sword).strip().replace('\n', ' '))
			seqs.append(seq)
			print(stc)
			print(seq)
			# print(np.array(sword)[np.where(np.array(seq) == 1)[0]])
			# print()

		# print(context)
		# print(np.array(cwords)[np.where(np.array(res) == 1)[0]])
		# print('======')

sentences = np.array(sentences)
seqs = np.array(seqs)
train_size = int(len(sentences) * 0.7)
dev_size = int(len(sentences) * 0.2)
test_size = int(len(sentences) * 0.1)
train_indices = np.random.choice(list(range(len(sentences))), train_size, replace=False)
dev_and_test_indices = list(set(range(len(sentences))) - set(train_indices))
dev_indices = np.random.choice(dev_and_test_indices, dev_size, replace=False)
test_indices = list(set(dev_and_test_indices) - set(dev_indices))


def save_sentences(filename, sentences_):
	print('Writing %d sentences to %s...' % (len(sentences_), filename))
	with open('data/%s.txt' % filename, 'w', encoding='utf-8') as f:
		for item in sentences_:
			f.write(item + '\n')

def save_labels(filename, seqs_):
	print('Writing %d sequences to %s...' % (len(seqs_), filename))
	with open('data/%s.txt' % filename, 'w') as f:
		for s in seqs_:
			f.write(' '.join(str(x) for x in s) + '\n')

save_sentences('train-sentences', sentences[train_indices])
save_labels('train-labels', seqs[train_indices])
save_sentences('dev-sentences', sentences[dev_indices])
save_labels('dev-labels', seqs[dev_indices])
save_sentences('test-sentences', sentences[test_indices])
save_labels('test-labels', seqs[test_indices])
