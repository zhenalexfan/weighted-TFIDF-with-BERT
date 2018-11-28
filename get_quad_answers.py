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
			sentences.append(' '.join(sword))
			seqs.append(seq)
			print(stc)
			print(seq)
			# print(np.array(sword)[np.where(np.array(seq) == 1)[0]])
			# print()

		# print(context)
		# print(np.array(cwords)[np.where(np.array(res) == 1)[0]])
		# print('======')

print('Printing %d sentences...' % len(sentences))
with open('data/quad_train_sentences.txt', 'w', encoding='utf-8') as f:
	f.writelines( "%s\n" % item for item in sentences)

print('Printing %d sequences...' % len(seqs))
with open('data/quad_train_ask_or_not.txt', 'w') as f:
	for seq in seqs:
		f.write(' '.join(str(x) for x in seq) + '\n')
