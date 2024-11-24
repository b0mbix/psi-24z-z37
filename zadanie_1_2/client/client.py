import socket
import sys

HOST = 'z37_zadanie1_2_python_server'
size = 512
BUFSIZE = 1024
port = 8000
message_no = 500

if len(sys.argv) >= 2:
    HOST = sys.argv[1]
if len(sys.argv) >= 3:
    port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print("Starting client job...")
    message_sent = 0
    message_successfully_sent = 0
    ack = 0
    while(True):
        ack ^= 1 #xor makes ack change between 0 and 1
        msg_length = size - 3
        msg = ''.join([chr(65 + i % 26) for i in range(msg_length)])
        datagram = ack.to_bytes(1, byteorder = 'big') + size.to_bytes(2, byteorder = 'big') + msg.encode('ascii')

        s.sendto(datagram, (HOST, port))

        message_sent += 1

        data, _ = s.recvfrom(size)
        while(data[0] - ord('0') != ack):
            s.sendto(datagram, (HOST, port))
            message_sent += 1
            data, _ = s.recvfrom(size)
        message_successfully_sent += 1
        print(f"Successfully sent datagram no {message_successfully_sent} of size {size}. Sent total of {message_sent} messages.")
