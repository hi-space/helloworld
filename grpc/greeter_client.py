import grpc

from protos import greeter_pb2 as pb2
from protos import greeter_pb2_grpc as rpc


if __name__ == '__main__':    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = rpc.GreeterStub(channel)
        request_data = pb2.Request(name="yoo")
        response = stub.Hello(request_data)

    print("received message: " + response.message)