import json
import string
import numpy as np
import spacy
import re
from termcolor import colored

# load data
data = []
with open('data/train-v2.0.json') as f:
	data = json.load(f)['data']

questions = []

for idx, datum in enumerate(data[:]):
	paras = datum['paragraphs']
	for p in paras:
		qas = p['qas']
		for qa in qas:
			question = qa['question']
			questions.append(question)
	print('Finish %d in %d' % (idx, len(data)))


def save_sentences(filename, sentences_):
	print('Writing %d sentences to %s...' % (len(sentences_), filename))
	with open('data/SQuAD/%s.txt' % filename, 'w', encoding='utf-8') as f:
		for item in sentences_:
			f.write(item + '\n')


save_sentences('questions', questions)
