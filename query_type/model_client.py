from __future__ import print_function

import grpc

import query_pb2_grpc
import query_pb2

QUERY_TYPE_WORDS = 0
QUERY_TYPE_SENTENCE = 1

def get_query_type(query):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = query_pb2_grpc.SentQueryStub(channel)
        response = stub.ReturnResult(query_pb2.Query(user_input=query))
    print("Client received: " + response.sent_type)
    return QUERY_TYPE_WORDS if "words" == response.sent_type else QUERY_TYPE_SENTENCE

if __name__ == '__main__':
    get_query_type("who is the ceo of apple")
