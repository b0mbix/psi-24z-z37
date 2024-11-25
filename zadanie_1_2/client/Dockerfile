FROM python:3
RUN apt-get update && apt-get install -y iproute2
ADD client.py /
ENTRYPOINT [ "python", "./client.py", "z37_zadanie1_2_python_server" ]

