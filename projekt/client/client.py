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

def construct_encrypted_message(session_key, msg_no, msg_content, msg_length_prefix=None):
    session_key_bytes = str(session_key).encode('ascii')
    otp = generate_otp(session_key, msg_no, len(msg_content))
    encrypted_msg_content = encrypt_message(msg_content, otp)
    mac = hmac.new(session_key_bytes, encrypted_msg_content, hashlib.sha256).digest()

    if msg_length_prefix:
        msg_length_bytes = msg_length.to_bytes(2, byteorder='big')
        return msg_length_bytes + b'|' + encrypted_msg_content + b'|' + mac
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
msg_length = 5
msg_prefix = f'{msg_length}|'
msg_content = ''.join([chr(65 + i % 26) for i in range(msg_length)])
endsession_msg = f'EndSession'

def connect_to_server(s):
    s.connect((HOST, port))
    s.sendall(hello_msg.encode('ascii'))
    response = s.recv(1024).decode('ascii')
    parts = response.split('|')
    if len(parts) == 2:
        if parts[0] != 'ServerHello':
            s.close()
    print(f"Connected to {HOST}:{port}")
    server_public_key = int(parts[1])
    session_key = calculate_session_key(server_public_key, private_key, module)
    return session_key

def send_message(s, session_key, msg_no):
    encrypted_msg = construct_encrypted_message(session_key, msg_no, msg_content, msg_length_prefix=msg_length)
    s.sendall(encrypted_msg)
    print(f"Encrypted {msg_content} message sent.")

def break_connection(s, session_key, msg_no):
    encrypted_end_session = construct_encrypted_message(session_key, msg_no, endsession_msg)
    s.sendall(encrypted_end_session)
    print("Encrypted EndSession message sent.")

def handle_response(s):
    pass


def interactive_client(s, session_key):
    msg_no = 1
    while True:
        print("\nChoose an action:")
        print("1. Send a message")
        print("2. Close the connection")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            send_message(s, session_key, msg_no)
            response = s.recv(1024).decode('ascii')
            if not response:
                print("Server has closed the connection.")
                break
            print(f"Server response: {response}")
            msg_no += 1
        elif choice == "2":
            break_connection(s, session_key, msg_no)
            response = s.recv(1024).decode('ascii')
            if not response:
                print("Server has closed the connection.")
                break
            print(f"Server response: {response}")
            print("Closing connection.")
            break
        else:
            print("Invalid choice. Please try again.")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting client...")
    session_key = connect_to_server(s)
    interactive_client(s, session_key)
    s.close()
    print("Client terminated.")
