docker rm -f z37_zadanie1_1_c_client
docker rmi -f z37_zadanie1_1_c_client

docker build -t z37_zadanie1_1_c_client .

docker run -it --hostname z37_zadanie1_1_c_client --network z37_network --name z37_zadanie1_1_c_client z37_zadanie1_1_c_client $1 $2
