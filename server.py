import socket
from gamesession import GameSession
from listentoclient import ListenToClient
from sendtoclient import SendToClient
from threading import Thread
import select


class Server(Thread):
    def __init__(self, host='', port=12800):
        Thread.__init__(self)
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.__host, self.__port))
        self.__clientlist = []  # List of clients
        self.__clientlisteners = []  # List of client listeners objects
        self.__clientsenders = []
        self.__maxclients = 2

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
        self.__sock.listen(self.__maxclients)
        while len(self.__clientlist) < self.__maxclients and self.__waiting:
            connection_in_queue, wlist, xlist = select.select([self.__sock], [], [], 0.05)
            for connection in connection_in_queue:
                client, address = connection.accept()
                self.__clientlist.append(client)
                print(client)
                self.gamesession.newplayer(client)
                self.__clientlisteners.append(ListenToClient(client, self.gamesession, len(self.__clientlist)))
                self.__clientsenders.append(SendToClient(client, self.gamesession, len(self.__clientlist)))
        print('here')
        if self.__waiting:
            for clientlistener in self.__clientlisteners:
                clientlistener.start()
            for clientsender in self.__clientsenders:
                clientsender.start()
            self.gamesession.start()
            self.gamesession.join()
        self.__sock.close()
        print('out in server')



if __name__ == "__main__":
    Server('', 12800).run()
