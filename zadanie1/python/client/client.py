import socket
import sys

HOST = '127.0.0.1'
size = 2
BUFSIZE = 1024

if len(sys.argv) < 3:
	port = 8000
else:
	HOST = int(sys.argv[1])
	port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	while True:
		msg_length = size - 2
		msg_array = ''.join([ascii(65 + i % 26) for i in range(msg_length)])
		datagram = size.to_bytes(2) + msg.encode('ascii')
		s.sendto(datagram, (HOST, port))

		data = s.recv(size)
		print("sending buffer size = ", size)
		size = size * 2
