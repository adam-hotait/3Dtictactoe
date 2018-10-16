import socket
from gamesession import GameSession
from listentoclient import ListenToClient


class Server:
    def __init__(self, host='', port=12800):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.clientlist = []  # List of clients
        self.clientlisteners = []  # List of client listeners objects
        self.maxclients = 2
        self.gamesession = GameSession()

    def listen(self):
        self.sock.listen(self.maxclients)
        while len(self.clientlist) < self.maxclients:
            client, address = self.sock.accept()
            client.settimeout(60)
            self.clientlist.append(client)
            print(client)
            if len(self.clientlist) == 1:
                self.gamesession.start()
            self.gamesession.newplayer(client)
            self.clientlisteners.append(ListenToClient(client, address, self.gamesession))
        for clientlistener in self.clientlisteners:
            clientlistener.start()
        self.gamesession.join()


if __name__ == "__main__":
    Server('', 12800).listen()
