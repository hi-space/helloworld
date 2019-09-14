from concurrent import futures

import grpc

import greeter_pb2 as pb2
import greeter_pb2_grpc as rpc


class GreeterServicer(rpc.GreeterServicer):
    def Hello(self, request, context):
        return pb2.Reply(message='Hello Response')

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
