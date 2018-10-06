import socket


class Client:
    def __init__(self, host = 'localhost', port = 12800):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self.active_connection = True
        print('Created client.')

    def be(self):
        msg = input('Message : ')
        self._socket.send(msg.encode())
        rcv = self._socket.recv(1024)
        print('Reçu :{}'.format(rcv.decode()))


if __name__ == "__main__":
    Client().be()