from concurrent import futures
import time as times
from time import time

import spacy
from benepar.spacy_plugin import BeneparComponent
import grpc
import query_pb2_grpc
import query_pb2


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Query(query_pb2_grpc.SentQueryServicer):
    def __init__(self, model_name='en'):
        load_t0 = time()
        print("load model file")
        # load spacy basic model1
        self.nlp = spacy.load(model_name)
        self.nlp.add_pipe(BeneparComponent('benepar_en_small'))
        load_t1 = time()

        print('* load model time: {:.2f}ms'.format((load_t1 - load_t0) * 1000))

    def ReturnResult(self, request, context):
        return query_pb2.Reply(sent_type=self.detect_input(request.user_input))

    def detect_input(self, user_input):
        doc = self.nlp(user_input)
        deps = [token.dep_ for token in doc]
        tags = [token.tag_ for token in doc]
        is_all_noun = ["NNP" == x for x in tags]
        sent = list(doc.sents)[0]
        constituency = sent._.parse_string

        if "nsubj" in deps and not all(is_all_noun):
            if "SBARQ" in constituency:
                return "query"
            else:
                return "sentence"
        else:
            return "words"


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    query_pb2_grpc.add_SentQueryServicer_to_server(Query(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            times.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
