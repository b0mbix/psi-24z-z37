
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

HOST = '0.0.0.0' #'z37_zadanie2_python_server'
BUFSIZE = 100000
port = 8000

if len(sys.argv) >= 2:
	port = int(sys.argv[1])

print(f"Listening on {HOST}:{port}")

def serve_client(conn, addr, thread_no):
	with conn:
		print('Connect from: ', addr)
		recv_size = 0
		while True:
			data = conn.recv( BUFSIZE )
			recv_size += len(data)
			if not data:
				print(f"Connection from thread{thread_no} closed?")
				break
			print(f"Received {recv_size} bytes in total from thread {thread_no}")
			conn.sendall(str(recv_size).encode('ascii'))
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
