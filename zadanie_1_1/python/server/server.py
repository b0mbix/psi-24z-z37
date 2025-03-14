import socket
import sys

HOST = '0.0.0.0' #'z37_zadanie1_1_python_server'
BUFSIZE = 1024
port = 8000

if len(sys.argv) >= 2:
	port = int(sys.argv[1])

print(f"Listening on {HOST}:{port}")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	s.bind((HOST, port))
	i = 1
	while True:
		data, address = s.recvfrom(BUFSIZE)
		#print(data)
		#print(address)

		if not data:
			print("Error in datagram?")
			s.sendto("Error in datagram?".encode('ascii'), address)
			break

		length = int.from_bytes(data[:2], byteorder = 'big')

		print(f"Received message no {i} of size {length}")
		s.sendto(f"Received message no {i} of size {length}".encode('ascii'), address)

		i += 1
