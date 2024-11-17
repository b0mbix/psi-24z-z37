import socket
import sys

HOST = 'z37_zadanie1_1_python_server'
size = 65500
BUFSIZE = 1024
port = 8000

if len(sys.argv) >= 2:
    HOST = sys.argv[1]
if len(sys.argv) >= 3:
	port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	while True:
		msg_length = size - 2
		msg = ''.join([chr(65 + i % 26) for i in range(msg_length)])
		datagram = size.to_bytes(2, byteorder = 'big') + msg.encode('ascii')

		s.sendto(datagram, (HOST, port))

		data = s.recv(size)
		print(f"Successfully sent gatagram of size {size}")

		size = size + 1
