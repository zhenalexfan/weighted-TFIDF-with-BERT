import json
import string
import numpy as np
import spacy
import re

nlp = spacy.load('en')

def check_token_numbers(s_file, l_file):
	sentences = []
	labels = []
	with open('data/SQuAD/%s.txt' % s_file, encoding='utf8') as f:
		sentences = f.read().split('\n')
	with open('data/SQuAD/%s.txt' % l_file, encoding='utf8') as f:
		labels = f.read().split('\n')
		labels = [x.strip().split(' ') for x in labels]
		print(len(sentences), len(labels))
		# print(labels[10])
	assert len(sentences) == len(labels)
	for i in range(len(sentences)):
		try:
			tokens = nlp(sentences[i])
			assert len(tokens) == len(labels[i])
		except AssertionError as e:
			print(len(tokens), [token.text for token in tokens])
			print(len(labels[i]), labels[i])
			print()
		# else:
		# 	print('yes')


check_token_numbers('sentences-remove-zeros', 'labels-remove-zeros')