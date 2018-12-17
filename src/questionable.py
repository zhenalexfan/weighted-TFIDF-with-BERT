# This is for SQuAD data

import spacy
import numpy as np

nlp = spacy.load('en')

with open('../data/SQuAD/sentences-remove-zeros.txt', 'r', encoding='utf8') as f:
    sents = f.read().split('\n')
with open('../data/SQuAD/labels-remove-zeros.txt', 'r') as f:
    labels = f.read().split('\n')
    labels = [line.strip().split(' ') for line in labels]
    for i in range(len(labels)):
        for j in range(len(labels[i])):
            labels[i][j] = 1 if labels[i][j] == '1' else 0

# checking validation
# assert len(sents) == len(labels)
# for i in range(len(sents)):
#     try:
#         tokens = nlp(sents[i])
#         assert len(tokens) == len(labels[i])
#     except AssertionError as e:
#         print(len(tokens), [token.text for token in tokens])
#         print(len(labels[i]), labels[i])
#         print()

def get_sentence(idx):
    return sents[idx]


def get_label(idx):
    return label[idx]


def get_questionable_tokens(idx):
    tokens = nlp(sents[idx])
    # text_questionable_tokens = []
    # for i, t in enumerate(tokens):
    #     if (labels[idx][i] == 1):
    #         text_questionable_tokens.append(t.text.lower())
    text_tokens = np.array([t.text.lower() for t in tokens])
    questionable_indices = np.where(np.array(labels[idx]) == 1)[0]
    text_questionable_tokens = text_tokens[questionable_indices]
    return text_questionable_tokens


def is_in_questionable_part(idx, query_word):
    return query_word in get_questionable_tokens(idx)
    # query_word = query_word.lower()
    # text_tokens = [t.text.lower() for t in nlp(sents[idx])]
    # text_tokens = np.array(text_tokens)
    # qword_indices = np.where(text_tokens == query_word)[0]
    # for qi in qword_indices:
    #     if labels[idx][qi] == True:
    #         return True
    # return False


if __name__ == '__main__':
    print(sents[1])
    print(labels[1])
    print(get_questionable_tokens(1))
    print(is_in_questionable_part(1, 'knowles'))
