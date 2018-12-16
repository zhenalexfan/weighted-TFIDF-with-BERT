import query_type_client
import tfidf_search
import bert_sim_search
import logging

STRATEGY_TO = "PLAIN TF-IDF ONLY"
STRATEGY_TB = "PLAIN TF-IDF + BERT"
STRATEGY_WB = "WEIGHTED TF-IDF + BERT"
SEARCH_STRATEGY = STRATEGY_WB

command_map = {
    'to': STRATEGY_TO,
    'tfidf-only': STRATEGY_TO,
    'tb': STRATEGY_TB,
    'tfidf+bert': STRATEGY_TB,
    'wb': STRATEGY_WB,
    'weighted+bert': STRATEGY_WB
}

RESULT_NUM = 10

all_sentences = bert_sim_search.sents


def truncate(query):
    return (query[:18] + '..') if len(query) > 20 else query


def search_to(query):
    print('Searching "%s" with PLAIN TF-IDF...' % truncate(query))
    sents, scores = tfidf_search.search(query, RESULT_NUM, weighted=False)
    logging.debug('Results: \t%s, \nScore: \t%s' % (str(sents), str(scores)))
    return sents


def search_tb(query):
    query_type = query_type_client.get_query_type(query)
    if query_type == query_type_client.QUERY_TYPE_WORDS:
        print('Searching "%s" with PLAIN TF-IDF...' % truncate(query))
        sents, scores = tfidf_search.search(query, RESULT_NUM, weighted=False)
    elif query_type == query_type_client.QUERY_TYPE_SENTENCE:
        print('Searching "%s" with PLAIN TF-IDF + BERT...' % truncate(query))
        p_sents, p_scores = tfidf_search.search(query, RESULT_NUM*10, weighted=False)
        sents, sims = bert_sim_search.search_in_range(query, RESULT_NUM, data_subset=p_sents)
    return sents


def search_wb(query):
    query_type = query_type_client.get_query_type(query)
    if query_type == query_type_client.QUERY_TYPE_WORDS:
        print('Searching "%s" with WEIGHTED TF-IDF...' % truncate(query))
        sents, scores = tfidf_search.search(query, RESULT_NUM, weighted=True)
    elif query_type == query_type_client.QUERY_TYPE_SENTENCE:
        print('Searching "%s" with WEIGHTED TF-IDF + BERT...' % truncate(query))
        p_sents, p_scores = tfidf_search.search(query, RESULT_NUM*10, weighted=True)
        sents, sims = bert_sim_search.search_in_range(query, RESULT_NUM, data_subset=p_sents)
    return sents


# instructions
INSTRUCTIONS = """
    INSTRUCTIONS

    Please type in a command or a query. A command is for selecting searching
    strategy for the following queries; a query is anything you would like to
    search.

    A command must start with '!'.

      Currently there are 3 different strategies for searching:
        !to | !tfidf-only    \t: using plain TF-IDF model only for results;
        !tb | !tfidf+bert    \t: using plainTF-IDF model for potential results and
          refine them with BERT vectors similarity when possible;
        !wb | !weighted+bert \t: using weighted TF-IDF model for potential results
          and refine them with BERT vectors similarity when possible.

      You can also use commands for:
        !result-num <number> \t: changing maximum search result number;
        !exit                \t: terminating this program.

    A query starts with anything except '!'.
"""
# TODO: commands for result number and so on

def main():
    print(INSTRUCTIONS)
    global SEARCH_STRATEGY
    global RESULT_NUM
    while True:
        query = input('Input anything >> ').strip().lower()
        if query == '':
            continue
        elif query == '!exit':
            break
        elif query[0] == '!':
            if query[1:] in command_map.keys():
                SEARCH_STRATEGY = command_map[query[1:]]
                print('You have switched to %s. ' % SEARCH_STRATEGY)
            elif 'result-num' in query[1:] and query[11:].strip().isdigit():
                n = int(query[11:].strip())
                RESULT_NUM = n
                print('You have set result number to %d. ' % n)
            else:
                print('Invalid command. ')
            print()
            continue
        else:
            if SEARCH_STRATEGY == STRATEGY_TO:
                sents = search_to(query)
            if SEARCH_STRATEGY == STRATEGY_TB:
                sents = search_tb(query)
            if SEARCH_STRATEGY == STRATEGY_WB:
                sents = search_wb(query)
            print()

            if len(sents) == 0:
                print('Ooops, nothing found.\n')
            else:
                for i, sent in enumerate(sents):
                    print('%3d. %s' % (i + 1, all_sentences[sent]))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
