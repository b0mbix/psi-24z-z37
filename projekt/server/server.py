import socket
import sys
from concurrent.futures import ThreadPoolExecutor
import hmac
import hashlib
import random

def calculate_public_key(base, private_key, module):
    (base ** private_key) % module

def calculate_session_key(foreign_public_key, own_private_key, module):
    (foreign_public_key ** own_private_key) % module

def generate_otp(session_key, msg_no, msg_len):
    seed = session_key + msg_no
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(msg_len)]

def encrypt_message(message, otp):
    return bytes(ord(char) ^ otp[i] for i, char in enumerate(message))

def decrypt_message(encrypted_message, otp):
    return ''.join(chr(byte ^ otp[i]) for i, byte in enumerate(encrypted_message))

def construct_encrypted_message(session_key, msg_no, msg_content, msg_prefix=None):
    session_key_bytes = str(session_key).encode('ascii')
    otp = generate_otp(session_key, msg_no, len(msg_content))
    encrypted_msg_content = encrypt_message(msg_content, otp)
    mac = hmac.new(session_key_bytes, encrypted_msg_content, hashlib.sha256).digest()

    if msg_prefix:
        prefix = msg_prefix.encode('ascii')
        return prefix + encrypted_msg_content + b'|' + mac
    else:
        return encrypted_msg_content + b'|' + mac

def verify_mac(received_message, received_mac, session_key):
    session_key_bytes = str(session_key).encode('ascii')
    computed_mac = hmac.new(session_key_bytes, received_message, hashlib.sha256).digest()
    return computed_mac == received_mac

HOST = '0.0.0.0' #'z37_projekt_server'
BUFSIZE = 1024
port = 8000
max_connections = 5
private_key = 3

if len(sys.argv) >= 2:
    port = int(sys.argv[1])
if len(sys.argv) >= 3:
    max_connections = int(sys.argv[2])

print(f"Listening on {HOST}:{port}")

def serve_client(conn, addr, thread_no):
    received_base = -1
    received_module = -1
    with conn:
        # HANDLING CLIENT HELLO
        print('Connect from: ', addr)
        data = conn.recv( BUFSIZE )
        if not data:
            print(f"Connection from thread {thread_no} closed?")
            conn.close()

        print(f"Received {data} fron {thread_no}")
        data = data.decode('ascii')

        if data[:11] == 'ClientHello':
            parts = data.split("|")
            received_base = int(parts[1])
            received_module = int(parts[2])
            client_public_key = int(parts[3])
            public_key = calculate_public_key(received_base, private_key, received_module)
            session_key = calculate_session_key(client_public_key, private_key, received_module)
            hello_msg = f"ServerHello|{public_key}"
            conn.sendall(hello_msg.encode('ascii'))
            print(f"Hello success")

        # HANDLING TARGET MESSAGE
        msg_content = ''
        msg_len = 0
        msg_no = 1
        expected_msg_len = -1
        while True:
            data = conn.recv( BUFSIZE )
            if not data:
                print(f"Connection from thread {thread_no} closed?")
                break

            if expected_msg_len == -1:
                msg_prefix = data.decode('ascii')
                parts = msg_prefix.split("|")
                if len(parts[0]) == 10:
                    if parts[0] == 'EndSession':
                        print(f"Received EndSession message from {thread_no}")
                        break
                expected_msg_len = parts[0]
                msg_content += parts[1]
                msg_len += len(msg_content)
                print(expected_msg_len)
                print(f"Received {msg_len} bytes in total from thread {thread_no}")

            else:
                msg_content += data.decode('ascii')
                if msg_len == expected_msg_len + 34 + len(str(expected_msg_len)):
                    print(f"Received whole message from thread {thread_no}")
                    mac = msg_content[:-32]
                    msg_content = msg_content[:-33]
                    if verify_mac(msg_content, mac, session_key):
                        print(f"Message integrity and authenticity confirmed")
                        otp = generate_otp(session_key, msg_no, len(msg_content))
                        encrypted_msg_content = decrypt_message(msg_content[:-1], msg_no, len(msg_content))
                        print(f"Received message content: {encrypted_msg_content} from {thread_no}")
                        break
                    else:
                        print(f"Message integrity and authenticity compromised")
                        break

        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, port))
    # the number of unaccepted connections that the system will allow before refusing new connections
    s.listen(max_connections)

    with ThreadPoolExecutor(max_connections) as executor:
        i=1
        try:
            while True:
                conn, addr = s.accept()
                executor.submit(serve_client, conn, addr, i)
                i+=1
            executor.shutdown()
        except:
            ("Exiting manually...")
        