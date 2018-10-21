import socket
from gamesession import GameSession
from listentoclient import ListenToClient
from sendtoclient import SendToClient
from threading import Thread


class Server(Thread):
    def __init__(self, host='', port=12800):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.clientlist = []  # List of clients
        self.clientlisteners = []  # List of client listeners objects
        self.clientsenders = []
        self.maxclients = 2
        print("serveur demarre")
        self.gamesession = GameSession()
        print("gamesession cree")

    def run(self):
        self.sock.listen(self.maxclients)
        while len(self.clientlist) < self.maxclients:
            client, address = self.sock.accept()
            self.clientlist.append(client)
            print(client)
            if len(self.clientlist) == 1:
                self.gamesession.start()
            self.gamesession.newplayer(client)
            self.clientlisteners.append(ListenToClient(client, self.gamesession, len(self.clientlist)))
            self.clientsenders.append(SendToClient(client, self.gamesession))
        for clientlistener in self.clientlisteners:
            clientlistener.start()
        for clientsender in self.clientsenders:
            clientsender.start()
        self.gamesession.join()


if __name__ == "__main__":
    Server('', 12800).run()
