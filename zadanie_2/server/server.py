import socket
import sys
from concurrent.futures import ThreadPoolExecutor

HOST = '0.0.0.0' #'z37_zadanie2_python_server'
BUFSIZE = 1024
port = 8000

if len(sys.argv) >= 2:
        port = int(sys.argv[1])

print(f"Listening on {HOST}:{port}")

def serve_client(conn, addr, thread_no):
        with conn:
                print('Connect from: ', addr)
                msg = b''
                msg_len = 0
                while True:
                        data = conn.recv( BUFSIZE )
                        if not data:
                                print(f"Connection from thread {thread_no} closed?")
                                break
                        msg += data
                        msg_len += len(data)
                        print(f"Received {msg_len} bytes in total from thread {thread_no}")
                        if data[-4:] == b'DONE':
                                conn.sendall(str(msg_len).encode('ascii'))
                                print(f"Success")
                                break
                conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        # the number of unaccepted connections that the system will allow before refusing new connections
        conn_nr = 5
        s.listen(conn_nr)

        with ThreadPoolExecutor(max_workers=5) as executor:
                i=1
                try:
                        while True:
                                conn, addr = s.accept()
                                executor.submit(serve_client, conn, addr, i)
                                i+=1
                        executor.shutdown()
                except:
                        ("Exiting manually...")
