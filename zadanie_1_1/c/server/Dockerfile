FROM gcc:4.9
COPY . /Server
WORKDIR /Server/
RUN gcc -o server server.c
CMD ["./server"]

