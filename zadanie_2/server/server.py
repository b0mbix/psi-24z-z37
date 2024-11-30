
import socket
import sys

HOST = '0.0.0.0' #'z37_zadanie2_python_server'
BUFSIZE = 100000
port = 8000

if len(sys.argv) >= 2:
	port = int(sys.argv[1])

print(f"Listening on {HOST}:{port}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, port))
	# the number of unaccepted connections that the system will allow before refusing new connections
	conn_nr = 5
	s.listen(conn_nr)

	while True:
		conn, addr = s.accept()
		with conn:
			print('Connect from: ', addr)
			i=1
			while True:
				data = conn.recv( BUFSIZE )

				if not data:
					print("Error in stream?")
					conn.sendall("Error in datagram?".encode('ascii'))
					break

				print(f"Received message no {i}")
				conn.sendall(f"Received message no {i}".encode('ascii'))
				i+=1
		conn.close()

print("Connection closed by client" )
