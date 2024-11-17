docker rm -f z37_zadanie1_1_c_server
docker rmi -f z37_zadanie1_1_c_server

docker build -t z37_zadanie1_1_c_server .

docker run -it --hostname z37_zadanie1_1_c_server --network z37_network --name z37_zadanie1_1_c_server z37_zadanie1_1_c_server $1
