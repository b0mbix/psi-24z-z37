#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netdb.h>

#define BUFSIZE 100000

void handle_sigint(int sig) {
        exit(0);
}

int main(int argc, char **argv) {
	int port = 8000, s;
	int i;
	int size_index;
	int size;
	int sizes = {2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,40000,48000,56000,60000,64000,65000,65200,65400,65500,65502,65504,65505,65506,65507};
	// char* server_hostname = "z37_zadanie1_1_python_server";
	char* server_hostname = "z37_zadanie1_1_c_server";
	struct sockaddr_in server;
	struct addrinfo hints, *res;
	struct sockaddr_storage client_address;
	socklen_t server_len; 
	char buffer[BUFSIZE];

	if (argc >= 2) {
		server_hostname = argv[1];
	} if (argc >= 3) {
		port = atoi(argv[2]);
	}

	// handle Ctrl+C
        signal(SIGINT, handle_sigint);

	if ((s = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
                perror("Socket failure?\n");
                exit(1);
	}

	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_DGRAM;
	if (getaddrinfo(server_hostname, NULL, &hints, &res) != 0) {
		perror("Unknown host failure\n");
		exit(0);
	}

	server = *(struct sockaddr_in *)res->ai_addr;
        server.sin_port = htons(port);

	freeaddrinfo(res);

	server_len = sizeof(server);
	
	printf("Starting client job...\n");
	for(size_index = 0; size_index < sizeof(sizes); size_index++) {
		size = sizes[size_index];
		buffer[0] = (size >> 8) & 0xff;
		buffer[1] = size & 0xff;
		for (i=0; i<=size; i++) {
			buffer[2+i] = 65 + i % 26;
		}


		if (sendto(s, buffer, size + 2, 0, (struct sockaddr *)&server, server_len) < 0){
			perror("sendto failure?\n");
			exit(1);
		}

		int len = recvfrom(s, buffer, BUFSIZE, 0, (struct sockaddr *)&server, &server_len);
        	if (len < 0) {
            		perror("recvfrom failure?\n");
           		exit(1);
        	}

		printf("Successfully sent datagram of size %d\n", size+2);
	}
	close(s);
}
