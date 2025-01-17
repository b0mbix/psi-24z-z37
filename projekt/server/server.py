import socket
import sys
from concurrent.futures import ThreadPoolExecutor

from cryptography_utils import calculate_public_key, calculate_session_key, generate_otp, encrypt_message, decrypt_message, construct_encrypted_message, verify_mac

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
    # the number of unaccepted connections that the system will allow before refusing new connections    s.listen(max_connections)

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
        