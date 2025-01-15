import socket
import sys
import hmac
import hashlib
import random

HOST = 'z37_projekt_server'
port = 8000

if len(sys.argv) >= 2:
    HOST = sys.argv[1]
if len(sys.argv) >= 3:
        port = int(sys.argv[2])

module = 23
base = 5
private_key = 4
public_key = (base ** private_key) % module

hello_msg = f'ClientHello|{base}|{module}|{public_key}'
msg_length = 50
msg_prefix = f'{msg_length}|'
msg_content = ''.join([chr(65 + i % 26) for i in range(msg_length)])
endsession_msg = f'EndSession'

def construct_encrypted_message(session_key, msg_no, msg_content, msg_prefix=None):
    encrypted_msg_content = encrypt_message(msg_content, generate_otp(session_key, msg_no, len(msg_c>    mac = hmac.new(session_key, encrypted_msg_content, hashlib.sha256).digest()
    if msg_prefix:
        return msg_prefix + encrypted_msg_content + '|' + mac
    else:
        return encrypted_msg_content + '|' + mac

def generate_otp(session_key, msg_no, msg_len):
    seed = session_key + msg_no
    return [random.randint(0, 255) for _ in range(msg_len)]

def encrypt_message(message, otp):
    return [m ^ k for m, k in zip(message, otp)]

def decrypt_message(encrypted_message, otp):
    return encrypt_message(encrypted_message, otp)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting client job...")
    s.connect((HOST, port))

    s.sendall(hello_msg.encode('ascii'))

    response = s.recv(1024).decode('ascii')

    parts = response.split('|')
    if parts[0] != 'ServerHello':
        s.close()
    server_public_key = int(parts[1])
    session_key = (server_public_key ** private_key) % module

    s.close()