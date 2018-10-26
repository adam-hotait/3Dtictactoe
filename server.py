import socket
from gamesession import GameSession
from listentoclient import ListenToClient
from sendtoclient import SendToClient
from threading import Thread
import select

# DEBUG
from threading import enumerate
from time import sleep


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

        # Bool that check if the server is in a waiting state, allows for server closure if quit during waiting for
        # clients loop
        self.__waiting = True
        print("serveur demarre")
        self.gamesession = GameSession()
        print("gamesession cree")

    def set_waiting_false(self):
        print('false set')
        self.__waiting = False

    def run(self):
        self.sock.listen(self.maxclients)
        while len(self.clientlist) < self.maxclients and self.__waiting:
            connection_in_queue, wlist, xlist = select.select([self.sock], [], [], 0.05)
            for connection in connection_in_queue:
                client, address = connection.accept()
                self.clientlist.append(client)
                print(client)
                self.gamesession.newplayer(client)
                self.clientlisteners.append(ListenToClient(client, self.gamesession, len(self.clientlist)))
                self.clientsenders.append(SendToClient(client, self.gamesession, len(self.clientlist)))
        print('here')
        if self.__waiting:
            for clientlistener in self.clientlisteners:
                clientlistener.start()
            for clientsender in self.clientsenders:
                clientsender.start()
            self.gamesession.start()
            self.gamesession.join()
        self.sock.close()
        print('out in server')



if __name__ == "__main__":
    Server('', 12800).run()
