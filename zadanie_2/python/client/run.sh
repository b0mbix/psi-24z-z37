docker rm -f z37_zadanie2_python_client1
docker rmi -f z37_zadanie2_python_client1

docker build -t z37_zadanie2_python_client1 .


docker rm -f z37_zadanie2_python_client2
docker rmi -f z37_zadanie2_python_client2

docker build -t z37_zadanie2_python_client2 .


docker rm -f z37_zadanie2_python_client3
docker rmi -f z37_zadanie2_python_client3

docker build -t z37_zadanie2_python_client3 .


docker run --hostname z37_zadanie2_python_client1 --network z37_network --name z37_zadanie2_python_client1 z37_zadanie2_python_client1 $1 $2 &
docker run --hostname z37_zadanie2_python_client2 --network z37_network --name z37_zadanie2_python_client2 z37_zadanie2_python_client2 $1 $2 &
docker run --hostname z37_zadanie2_python_client3 --network z37_network --name z37_zadanie2_python_client3 z37_zadanie2_python_client3 $1 $2 &

wait


echo 'Job finished'
