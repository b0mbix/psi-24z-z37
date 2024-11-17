#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>

const int BUFSIZE = 1024;

int main(int argc, char **argv)
{
	int port, s;
	int i = 1;
	int size = 0;
	struct sockaddr_in server;
	struct sockaddr_storage client_address;
	socklen_t client_address_length = sizeof(client_address_length);
	char ip[INET_ADDRSTRLEN];
	char buffer[BUFSIZE];

	if (argc < 3) {
		//perror("IP and port arguments expected!");
		//exit(1);
		strcpy(ip, "172.21.37.1");
		port = 8000;
	} else {
		strcpy(ip, inet_addr(argv[1]));
		port = atoi(argv[2]);
	}

	if ((s = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
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

	const char *message = "Hello, server!";
	uint16_t data_length = htons(strlen(message));
	memcpy(buffer, &data_length, sizeof(uint16_t));
	memcpy(buffer + sizeof(uint16_t), message, strlen(message));


	i = 1;
	size = 2;
	while(1) {

		if (sendto(s, buffer, sizeof(uint16_t) + strlen(message), 0, (struct sockaddr *)&server, sizeof(server)) < 0){
			perror("sendto failure?");
			exit(1);
		}


		/*if (recvfrom(s, buffer, BUF_SIZE, 0, (struct sockaddr *) &client_address, &client_address_length) < 0) {
			perror("recvfrom failure?");
			exit(1);
		}*/

		printf("Received message no %d of size %d, i, size");

		i += 1;
	}
	close(s);
}
