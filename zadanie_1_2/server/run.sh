docker rm -f z37_zadanie1_2_python_server
docker rmi -f z37_zadanie1_2_python_server

docker build -t z37_zadanie1_2_python_server .

docker run -it --hostname z37_zadanie1_2_python_server --network z37_network --name z37_zadanie1_2_python_server z37_zadanie1_2_python_server $1
