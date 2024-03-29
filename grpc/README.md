# installation

```sh
pip install grpcio
pip install grpcio-tools
```

# gRPC
- 분산시스템에서 다른 머신의 서버 어플리케이션에 있는 메소드를 자신이 갖고 있는 것 처럼 호출할 수 있게 해주는 프레임워크
- HTTP/2 기반으로 통신 
- IDL로 google Protocol Buffers 사용
- Server, Cilent 모두 sync, async 방식 제공
- 다양한 언어와 플랫폼 지원


## RPC
- Remote Procedure Call
- 원격 컴퓨터나 프로세스에 존재하는 함수를 호출하는데 사용하는 프로토콜
- 네트워크 상태나 콜 방식을 신경쓰지 않고 프로그래머가 원격의 함수를 실행하는 것

## HTTP/1
- Client가 Server에 Request 보내고 서버가 해당 Request에 대한 Response를 보내는 구조 (Request 단위로 Client - Server 왕복)
- Header에 Cookie가 포함되어 있어 헤더 크기가 크고 느리다.
  
## HTTP/2
- __Header Compression__ : Header Table과 Huffman Encoding 기법을 사용해서 헤더 정보를 압축
- __Multiplexed Streams__ : HTTP/1에서는 요청마다 새로운 connection을 자주 만들었는데, HTTP/2는 한개의 connection으로 동시에 여러개의 메시지를 주고받을 수 있다.
- __Server Push__ : Client 요청 없이도 서버가 Resource를 보낼 수 있다. (Client 요청이 최소화되어 성능 향상)
- __Stream Priority__ : Request에 우선순위를 지정하여 중요한 Resource를 먼저 전달받을 수 있다.
- 양방향 스트리밍이 가능해서 서버와 클라이언트가 서로 동시에 데이터를 스트리밍으로 주고 받을 수 있다. 
- HTTP 보다 헤더 압축률이 더 높고 ProtoBuf로 메시지를 정의해서 메시지 크기가 크게 줄어들었다. 이로 인해 네트워크 트래픽이 줄어들고 성능이 높아졌다.

# Build Proto

Define a service in a .proto file.

```sh
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/example.proto
```
```sh
python -m grpc_tools.protoc -I$SRC_DIR --python_out=$DST_DIR --grpc_python_out=$DST_DIR example.proto
```
ProtoBuf의 컴파일러인 protoc를 사용해 proto 파일을 빌드하게 되면,  pb2 파일, pb2_grpc 파일 2개가 생성된다.
  - `_pb2` : Data class
  - `_pb2_grpc` : Server, Client class
    - Stub:  Client가 RPC call 하기 위해서 사용
    - Servicer: Service 구현을 위한 인터페이스

## Service Method

### Simple RPC

```rpc
rpc GetFeature(Point) returns (Feature) {}
```
> the client sends a request to the server using the stub and waits for a response to come back, just like a normal function call.

- Client가 Server에 single request를 보내면, 서버는 single response를 리턴한다.

### Response-streaming RPC

```rpc
rpc ListFeatures(Rectangle) returns (stream Feature) {}
```

> the client sends a request to the server and gets a stream to read a sequence of messages back. The client reads from the returned stream until there are no more messages. As you can see in the example, you specify a response-streaming method by placing the stream keyword before the response type.

- 서버에서 클라이언트로 스트리밍하는 RPC
- Client가 Server에 single request를 보내면, 서버는 stream 을 리턴한다.
- Client는 더 이상의 message가 없을 때 까지 stream (sequence of messages)을 읽는다.

### Request-streaming RPC

```rpc
rpc RecordRoute(stream Point) returns (RouteSummary) {}
```

> the client writes a sequence of messages and sends them to the server, again using a provided stream. Once the client has finished writing the messages, it waits for the server to read them all and return its response. You specify a request-streaming method by placing the stream keyword before the request type.

- 클라이언트에서 서버로 스트리밍하는 RPC
- Client는 주어진 stream을 이용해 message sequence를 서버에 보낸다. 
- Client는 message를 모두 서버에 쓰고나면 Server의 Response 리턴을 기다린다.



### Bidirectional streaming RPC

```rpc
rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}
```

> both sides send a sequence of messages using a read-write stream. The two streams operate independently, so clients and servers can read and write in whatever order they like: for example, the server could wait to receive all the client messages before writing its responses, or it could alternately read a message then write a message, or some other combination of reads and writes. The order of messages in each stream is preserved. You specify this type of method by placing the stream keyword before both the request and the response.

- 양방향 스트리밍 RPC
- Server, Client 가 모두 message sequence를 보낸다.
- 두 stream은 독립적으로 동작하고, Server, Client는 원하는 순서대로 읽을 수 있다.
- Server는 Client의 모든 메시지를 읽은 뒤 Response를 return 할 수도 있고, 번갈아 가며 한 message 씩 읽고 쓸 수도 있다. (각 stream 에서 message 순서는 보존된다)

# Server-side

- Service 인터페이스를 구현 
- Client의 Request에 따라 Response를 리턴

```py
import grpc

import greeter_pb2 as pb2
import greeter_pb2_grpc as rpc
```

```py
class GreeterServicer(rpc.GreeterServicer):
    def Hello(self, request, context):
        return pb2.Reply(message='Hello Response')
```

Servicer 인터페이스를 상속받아서 서비스를 구현한다.

```py
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
rpc.add_GreeterServicer_to_server(GreeterServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
```

사용할 포트를 설정하고 `add_RouteGuideServicer_to_server` 함수를 이용해 구현한 서비스 `GreeterServicer` 를 `grpc.server`에 추가한다.

# Client-side

- Servicve 메소드 호출을 위해 Stub 생성

```py
with grpc.insecure_channel('localhost:50051') as channel:
    stub = rpc.GreeterStub(channel)
```

GreeterStub 클래스를 인스턴스화 한다.

```py
request_data = pb2.Request(name="yoo")
response = stub.Hello(request_data)
```

서비스의 메서드를 호출하고 Server로 부터 오는 response를 리턴받는다.

# Reference
- https://grpc.io/docs/tutorials/basic/python/
- https://developers.google.com/protocol-buffers/docs/proto3
- https://developers.google.com/protocol-buffers/docs/pythontutorial
- https://medium.com/@goinhacker/microservices-with-grpc-d504133d191d

### Codes

- [Python](https://grpc.io/docs/languages/python/basics/)
- [Go](https://github.com/grpc/grpc-go/blob/master/examples/route_guide/server/server.go)
