import socket
import sys

HOST = '127.0.0.1'
BUFSIZE = 4096

if len(sys.argv) < 3:
	port = 8000
else:
	HOST = int(sys.argv[1])
	port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	s.bind((HOST, port))
	i = 1
	while True:
		data, address = s.recvfrom(BUFSIZE)

		if not data:
			s.sendto("Error in datagram?", address)
			print("Error in datagram?")
			break

		length = int.from_bytes(data[:2])
		s.sendto(f"Received message {i} of size {length}", address)
		print(f"Received message {i} of size {length}")
		i += 1
