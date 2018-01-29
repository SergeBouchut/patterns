import socket
from threading import Thread

from dispatcher import CommandDispatcher as cmd


@cmd.register
def iam(name):
    return f'hello {name}'


@cmd.register
def ping():
    return 'pong'


@cmd.register
def quit():
    return 'bye'


def handle_client(client):
    request = None
    while request != 'quit':
        request = client.recv(255).decode('utf8')
        response = cmd.run(request)
        client.send(response.encode('utf8'))
    client.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 15555))
server.listen(8)

try:
    while True:
        client, _ = server.accept()
        Thread(target=handle_client, args=(client,)).start()
except KeyboardInterrupt:
    server.close()
