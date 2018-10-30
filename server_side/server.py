import socket
from .gamesession import GameSession
from .listentoclient import ListenToClient
from .sendtoclient import SendToClient
from threading import Thread
import select


class Server(Thread):
    """
    Server thread.
    It will:
    1) Create connections to/from clients
    2) Summon 'SendToClient' and 'ListenToClient' threads that are in charge of communications (1 each per client)
    3) Once two clients are connected, start all thread and start the game session.
    4) Join the game session.
    """
    def __init__(self, host='', port=12800):
        # The server is running in its own thread
        Thread.__init__(self)

        # Declaration of socket-related objects and variables
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.__host, self.__port))

        # Initialisation of client related objects
        self.__client_list = []  # List of clients socket connections
        self.__client_listeners = []  # List of client listeners objects
        self.__client_senders = []  # List of client senders objects
        self.__max_clients = 2

        # Creation of a game session
        self.game_session = GameSession()

        # Bool that check if the server is in a waiting state, allows for server closure if the host player quits
        # while the server is waiting for an incoming connection
        self.__waiting = True

        print('Server initialised')

    def set_waiting_false(self):
        """
        Method that allows to put the server out of its initial waiting class from outside the class.
        """
        self.__waiting = False

    def run(self):
        self.__sock.listen(self.__max_clients)  # The server listens to connection requests
        print('Server running and listening on port {}'.format(self.__port))
        while len(self.__client_list) < self.__max_clients and self.__waiting:
            connection_in_queue, wlist, xlist = select.select([self.__sock], [], [], 0.05)
            for connection in connection_in_queue:  # If there is a connection request
                client, address = connection.accept()  # Accept the request
                self.__client_list.append(client)

                print('Connected to client at address: {}'.format(address))

                # Summon a 'SendToClient' and a 'ListenToClient' instance to communicate with this client
                self.__client_listeners.append(ListenToClient(client, self.game_session, len(self.__client_list)))
                self.__client_senders.append(SendToClient(client, self.game_session, len(self.__client_list)))

        # When we get out of the 'Waiting for Clients' phase, we'll first check that it wasn't because the server
        # simply stopped waiting (ie. Server.set_waiting_false function was called).
        if self.__waiting:
            # We start all threads and join the game session.
            for client_listener in self.__client_listeners:
                client_listener.start()
                print('Started all listeners')
            for client_sender in self.__client_senders:
                client_sender.start()
                print('Started all senders')
            self.game_session.start()
            print('Started game session. Now joining it...')
            self.game_session.join()
        # At the end of the thread execution, the server can be stopped.
        self.__sock.close()
        print('Server closed.')


if __name__ == "__main__":
    Server('', 12800).run()
