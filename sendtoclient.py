import threading
import socket


class SendToClient(threading.Thread):
    """
    This class sends servers messages to the client.
    There is one dedicated instance per client.
    """
    def __init__(self, client, game_session, player_id):
        super().__init__()
        self.__client = client
        self.__game_session = game_session
        self.__size = 1024
        self.__player_id = player_id

    def run(self):
        client_open = True
        self.__client.send(b'NEW')
        self.__client.send(('INV' + self.__game_session.current_player).encode())
        while client_open:
            with self.__game_session.send_condition:
                self.__game_session.send_condition.wait()
                code = self.__game_session.response[0]
                player_id = self.__game_session.response[1]
                if code == 'SET':
                    i, j, k = self.__game_session.response[2]
                    self.__client.send((''.join(str(e) for e in [code, player_id, i, j, k])).encode())
                    self.__client.send(('INV' + self.__game_session.current_player).encode())
                if code == 'WIN':
                    i1, j1, k1 = self.__game_session.response[2]
                    i2, j2, k2 = self.__game_session.response[3]
                    i3, j3, k3 = self.__game_session.response[4]
                    self.__client.send((''.join(str(e) for e in [code, player_id, i1, j1, k1, i2, j2, k2, i3, j3, k3]))
                                       .encode())
                if code == 'RST':
                    print('RST')
                    self.__client.send(b'RST')
                    self.__client.send(('INV' + self.__game_session.current_player).encode())
                if code == 'QUT':
                    print('QUT')
                    self.__client.send(b'QUT')
                    self.__client.shutdown(socket.SHUT_RDWR)
                    self.__client.close()
                    client_open = False
                self.__game_session.set_semaphore()
