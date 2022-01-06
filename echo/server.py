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
            print(text)
            print('sending data back to the client')
            text_spl = text.split("\r\n")
            method_resp = text_spl[0].split(' ')
            method = method_resp[0]
            status = method_resp[1][9:]
            status_descr = "Status doesn't exist"
            for item in http.HTTPStatus:
                if str(item.value) == status:
                    status_descr = item.name
            body = f"Request method : {method}"
            request_source = text_spl[1].split(' ')[1]
            request_source = request_source.split(":")
            request_source[1] = int(request_source[1])
            request_source = tuple(request_source)
            body += f"<br />Request source: {request_source}"
            body += f"<br />Response status: {status} {status_descr}"

            text_spl.pop(0)
            text_spl.pop(0)
            for item in text_spl:
                body += f"<br />{item}"

            status_line = 'HTTP/1.1 200 OK'
            headers = '\r\n'.join([
                status_line,
                f'Content-Length: {len(body)}',
                'Content-Type: text/html'
            ])
            resp = '\r\n\r\n'.join([
                headers,
                body
            ])
            conn.send(resp.encode('utf-8'))
        conn.close()
