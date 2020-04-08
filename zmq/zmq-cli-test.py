import zmq, sys

ctx = zmq.Context()

def run_client(port=5555):
    sock = ctx.socket(zmq.REQ)
    sock.connect(f'tcp://15.165.181.111:{port}')
    while True:
        line = input()
        sock.send(line.encode())
        rep = sock.recv()
        print(f'Reply: {rep.decode()}')
        if rep.decode() == 'bye':
            sock.close()
            break

run_client(5555)