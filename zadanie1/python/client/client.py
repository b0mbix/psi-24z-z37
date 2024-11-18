import socket
import sys

# HOST = 'z37_zadanie1_1_python_server'
HOST = 'z37_zadanie1_1_c_server'
sizes = [2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,40000,48000,56000,60000,64000,65000,65200,65400,65500,65502,65504,65505,65506,65507]
BUFSIZE = 1024
port = 8000

if len(sys.argv) >= 2:
    HOST = sys.argv[1]
if len(sys.argv) >= 3:
	port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print("Starting client job...")
    for (size in sizes):
        msg_length = size - 2
        msg = ''.join([chr(65 + i % 26) for i in range(msg_length)])
        datagram = size.to_bytes(2, byteorder = 'big') + msg.encode('ascii')

        s.sendto(datagram, (HOST, port))

        data, _ = s.recvfrom(size)
        print(f"Successfully sent datagram of size {size}")
