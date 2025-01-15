import socket
import sys
from concurrent.futures import ThreadPoolExecutor

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
            # obsluzyc ten przypadek

        print(f"Received {data} fron {thread_no}")
        data = data.decode('ascii')

        if data[:11] == 'ClientHello':
            data = data.split("|")
            received_base = int(data[1])
            received_module = int(data[2])
            client_public_key = int(data[3])
            public_key = (received_base ** private_key) % received_module
            session_key = (client_public_key ** private_key) % received_module
            hello_msg = f"ServerHello|{public_key}"
            conn.sendall(hello_msg.encode('ascii'))
            print(f"Hello success")

        # HANDLING TARGET MESSAGE
        msg = b''
        msg_len = 0
        expected_msg_len = -1
        while True:
            data = conn.recv( BUFSIZE )
            if not data:
                print(f"Connection from thread {thread_no} closed?")
                break

            msg += data
            msg_len += len(data)
            if (expected_msg_len == -1):
                expected_msg_len = int.from_bytes(msg[:2], byteorder='big')

            print(f"Received {msg_len} bytes in total from thread {thread_no}")
            if msg_len == expected_msg_len + 36:
                print(f"Received whole message from thread {thread_no}")
                print(f"Message: {msg[2:-32]}")
                break

        # CHECKING MAC
        #expected_mac = msg[-32:].decode("ascii")
        #mac = -1 # ... obliczenia
        #if (mac == expected_mac):
        #        print(f"Message integrity and authenticity confirmed")

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
        