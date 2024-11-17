#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BUFSIZE 1024

int main(int argc, char **argv) {
	char* host = "0.0.0.0";
	int port = 8000, s;
	int i = 1;
	int size = 0;
	struct sockaddr_in server;
	struct sockaddr_storage client_address;
	socklen_t client_address_length = sizeof(client_address);
	char buffer[BUFSIZE];

	if (argc >= 2) {
		port = atoi(argv[1]);
	}

	if ((s = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
                perror("Socket failure?");
                exit(1);
	}

	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY; //'0.0.0.0'
	server.sin_port = htons(port);

	if (bind(s, (struct sockaddr *) &server, sizeof(server)) < 0) {
		perror("Binding failure?");
		exit(1);
	}

	printf("Listening on %s:%d\n", host, port);

	while(1) {
		if (recvfrom(s, buffer, BUFSIZE, 0, (struct sockaddr *)&client_address, &client_address_length) < 0) {
			perror("recvfrom failure");
			exit(1);
		}

		//printf(buffer)
		//printf(client_address)

		//process message

		printf("Received message no %d of size %d", i, size);

		//sendto

		i += 1;
	}
	close(s);
}
