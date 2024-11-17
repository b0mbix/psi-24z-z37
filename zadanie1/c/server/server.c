#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>

const int BUFSIZE = 1024;

int main(int argc, char **argv)
{
	int port, s;
	int i = 1
	int size = 0;
	struct sockaddr_in server;
	struct sockaddr_storage client_address;
	socklen_t client_address_length = sizeof(client_address_length);
	char buffer[BUFSIZE];

	if (argc < 2):
		port = 8000;
	else:
		port = atoi(argv[1]);

	if (s = socket(AF_INET, SOCKDGRAM, 0) < 0) {
                perror("Socket failure?");
                exit(1);
	}

	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY; //'0.0.0.0'
	server.sin_port = port;

	if (bind(s, (struct sockaddr *) &server, sizeof server) < 0) {
		perror("Binding failure?");
		exit(1);
	}

	i = 1;
	size = 0;
	while(True) {
		if (recvfrom(s, buffer, BUF_SIZE, 0, (struct sockaddr *) &client_address, &client_address_length) < 0) {
			perror("Socket failure?");
			exit(1);
		}

		//printf(buffer)
		//printf(client_address)

		//process message

		printf("Received message no %d of size %d, i, size")

		//sendto

		i += 1;
	}
	close(s);
}
