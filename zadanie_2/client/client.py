import socket
import sys

HOST = 'z37_zadanie2_python_server'
port = 8000

if len(sys.argv) >= 2:
    HOST = sys.argv[1]
if len(sys.argv) >= 3:
        port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting client job...")

    s.connect((HOST, port))

    msg_length = 1000000
    msg = ''.join([chr(65 + i % 26) for i in range(msg_length)])
    stream = msg.encode('ascii')
    s.sendall(stream)
    s.sendall(b'DONE')

    response = s.recv(1024).decode('ascii')
    s.close()
    print('Client finished.')
