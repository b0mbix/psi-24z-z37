import socket
import sys
import hmac

HOST = 'z37_zadanie2_server'
port = 8000

if len(sys.argv) >= 2:
    HOST = sys.argv[1]
if len(sys.argv) >= 3:
        port = int(sys.argv[2])

module = 23
base = 5
private_key = 4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting client job...")

    s.connect((HOST, port))

    public_key = (base ** private_key) % module

    hello_msg = f'ClientHello|{base}|{module}|{public_key}'

    s.sendall(hello_msg.encode('ascii'))


    response = s.recv(1024).decode('ascii')
    print(response)

    parts = response.split('|')

    if parts[0] == 'ServerHello':
        server_public_key = parts[1]

    print(response)
    #session_key = (server_public_key ** private_key) % module

    #mac = 'mimimimimimimimimimimimimimimimi'
    #msg_length = 50
    #msg_prefix = f'{msg_length}|'
    #msg_content = ''.join([chr(65 + i % 26) for i in range(msg_length)])

    s.close()
