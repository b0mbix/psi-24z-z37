import socket
import sys

from cryptography_utils import calculate_public_key, calculate_session_key, generate_otp, encrypt_message, decrypt_message, construct_encrypted_message, verify_mac

HOST = 'z37_projekt_server'
port = 8000

if len(sys.argv) >= 2:
    HOST = sys.argv[1]
if len(sys.argv) >= 3:
        port = int(sys.argv[2])

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

    msg_no = 2
    encrypted_end_session = construct_encrypted_message(session_key, msg_no, endsession_msg)
    s.sendall(encrypted_end_session)
    print("EndSession message sent.")

    s.close()