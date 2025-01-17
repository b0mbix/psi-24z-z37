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

def calculate_public_key(base, private_key, module):
    return (base ** private_key) % module

def calculate_session_key(foreign_public_key, own_private_key, module):
    return (foreign_public_key ** own_private_key) % module

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

module = 23
base = 5
private_key = 4
public_key = calculate_public_key(base, private_key, module)

hello_msg = f'ClientHello|{base}|{module}|{public_key}'
msg_length = 50
msg_prefix = f'{msg_length}|'
msg_content = ''.join([chr(65 + i % 26) for i in range(msg_length)])
endsession_msg = f'EndSession'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting client job...")
    s.connect((HOST, port))

    s.sendall(hello_msg.encode('ascii'))

    response = s.recv(1024).decode('ascii')

    parts = response.split('|')
    if parts[0] != 'ServerHello':
        s.close()
    server_public_key = int(parts[1])
    session_key = calculate_session_key(server_public_key, private_key, module)

    msg_no = 1
    encrypted_msg = construct_encrypted_message(session_key, msg_no, msg_content, msg_prefix=f'{msg_length}|')
    s.sendall(encrypted_msg)
    print(f"Encrypted message sent: {encrypted_msg}")

    #response2 = s.recv(1024)
    #print(response2)

    #msg_no = 1
    #encrypted_end_session = construct_encrypted_message(session_key, msg_no, endsession_msg)
    #s.sendall(encrypted_end_session)
    #print("EndSession message sent.")

    response3 = s.recv(1024)
    print(response3)

    s.close()
