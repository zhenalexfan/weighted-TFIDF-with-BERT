import bert_sim_search
import spacy
from termcolor import colored

with open('data/SQuAD/sentences-remove-zeros.txt', 'r', encoding='utf8') as f:
    sents = f.read().split('\n')
with open('data/SQuAD/labels-remove-zeros.txt', 'r') as f:
    labels = f.read().split('\n')
    labels = [line.strip().split(' ') for line in labels]
    for i in range(len(labels)):
        for j in range(len(labels[i])):
            labels[i][j] = 1 if labels[i][j] == '1' else 0

nlp = spacy.load('en')


def print_colored_sentence(sent, label):
    sent_ = nlp(sent)
    for token in sent_:
        if label[token.i] == 0:
            print(token.text_with_ws, end='')
        else:
            print(colored(token.text_with_ws, 'red'), end='')
    print()


while True:
    index = input('Index (0~%d): ' % len(sents)).strip()
    if index.isdigit():
        index = int(index)
        print_colored_sentence(sents[index], labels[index])
    else:
        print('Invalid index. ')
