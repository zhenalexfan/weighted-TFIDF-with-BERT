import main
import datetime

all_sentences = main.all_sentences


def precision(retrieved, tags, at=0):
    relevant = 0
    calc_len = len(retrieved) if at == 0 else at
    for s in retrieved[:calc_len]:
        if tags[s] == 1:
            relevant += 1
    return relevant / calc_len


def calc_precisions(retrieved, tags):
    return [precision(retrieved, tags, at=i) for i in [0, 3, 5, 7, 9]]


def get_all_precisions(sents_to, sents_wt, sents_wb, tags):
    return [
        calc_precisions(sents_to, tags),
        calc_precisions(sents_wt, tags),
        calc_precisions(sents_wb, tags)
    ]

def get_all_precisions_string(sents_to, sents_wt, sents_wb, tags):
    all_precisions = [
        calc_precisions(sents_to, tags),
        calc_precisions(sents_wt, tags),
        calc_precisions(sents_wb, tags)
    ]
    output = ''
    for p, ps in enumerate(['tf-idf', 'weighted', 'wei+bert']):
        for i, at in enumerate([0, 3, 5, 7, 9]):
            output += '%s p@%d: %.6f\n' % (ps, at, all_precisions[p][i])
    return output


def save_tag(filename, query, tags, all_precisions_string):
    tags = list(tags.items())
    output = '\n'.join(["%d %d" % (tags[i][0], tags[i][1]) for i in range(len(sents))])
    with open(filename, 'w') as f:
        f.write('Query: %s\n' % query)
        f.write(all_precisions_string)
        f.write(output)


while True:
    query = input('Query: ')
    if query == '':
        continue
    sents_to = main.search_to(query)
    sents_wt = main.search_wt(query)
    sents_wb = main.search_wb(query)

    sents = list(set(sents_to).union(set(sents_wt), set(sents_wb)))
    tags = dict()

    i = 0
    while i < len(sents):
        sent = sents[i]
        print()
        print('Query:', query)
        print('Sentence[%d]:' % sent, all_sentences[sent])
        relevant = input('Relevant? ')
        if relevant == '1':
            tags[sent] = 1
            i += 1
        elif relevant == '0':
            tags[sent] = 0
            i += 1
        else:
            continue
    filename = 'data/experiment-queries/%s.txt' % str(datetime.datetime.now())[11:]
    all_precisions_string = get_all_precisions_string(sents_to, sents_wt, sents_wb, tags)
    save_tag(filename, query, tags, all_precisions_string)
