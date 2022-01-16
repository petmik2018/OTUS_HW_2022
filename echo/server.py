import os
import socket
import http

from helpers import get_open_port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    srv_addr = ('', get_open_port())
    print(f'starting on {srv_addr}, pid: {os.getpid()}')

    s.bind(srv_addr)
    s.listen(1)

    while True:
        print('waiting for connection')
        conn, raddr = s.accept()
        print('connection from', raddr)

        while True:
            data = conn.recv(1024)
            text = data.decode('utf-8')
            if not text:
                print(f'no data from {raddr}')
                break
            print('sending data back to the client')
            text_spl = text.split("\r\n")
            method_resp = text_spl[0].split(' ')
            method = method_resp[0]
            status = method_resp[1][9:]
            try:
                status_name = http.HTTPStatus(int(status)).phrase
            except:
                status = "200"
                status_name = "OK"
            body = f"Request method : {method}"
            request_source = raddr
            body += f"\r\nRequest source: {request_source}"
            body += f"\r\nResponse status: {status} {status_name}"

            text_spl.pop(0)
            text_spl.pop(0)
            for item in text_spl:
                body += f"\r\n{item}"

            status_line = f'HTTP/1.1 {status} {status_name}'
            headers = '\r\n'.join([
                status_line,
                f'Content-Length: {len(body)}',
            ])
            resp = '\r\n\r\n'.join([
                headers,
                body
            ])
            conn.send(resp.encode('utf-8'))
        conn.close()
