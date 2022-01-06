import socket
import sys

PORT = None

try:
    PORT = int(sys.argv[1])

except IndexError:
    print("Pass a port for connection")
    exit(1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    srv_addr = ('127.0.0.1', PORT)
    print(f'connection to {srv_addr}')
    s.connect(srv_addr)

    sent_msg = 'GET /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:52759\r\nUser-Agent: Local'
    print(f'sending "{sent_msg}"')
    s.send(sent_msg.encode('utf-8'))

    recv_msg = s.recv(1024).decode('utf-8')
    print(f'received "{recv_msg}"')
