docker rm -f z37_zadanie1_2_python_client
docker rmi -f z37_zadanie1_2_python_client

docker build -t z37_zadanie1_2_python_client .

docker run -it --hostname z37_zadanie1_2_python_client --network z37_network --name z37_zadanie1_2_python_client z37_zadanie1_2_python_client $1 $2
