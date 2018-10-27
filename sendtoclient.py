import threading
import socket

class SendToClient(threading.Thread):
    def __init__(self, client, gamesession, player_id):
        super().__init__()
        print('init')
        self.__client = client
        self.__gamesession = gamesession
        self.__size = 1024
        self.__player_id = player_id

    def run(self):
        client_open = True
        self.__client.send(b'NEW')
        self.__client.send(('INV' + self.__gamesession.current_player).encode())
        while client_open:
            with self.__gamesession.send_condition:
                self.__gamesession.send_condition.wait()
                code = self.__gamesession.response[0]
                player_id = self.__gamesession.response[1]
                if code == 'SET':
                    i, j, k = self.__gamesession.response[2]
                    self.__client.send((''.join(str(e) for e in [code, player_id, i, j, k])).encode())
                    self.__client.send(('INV' + self.__gamesession.current_player).encode())
                if code == 'WIN':
                    i1, j1, k1 = self.__gamesession.response[2]
                    i2, j2, k2 = self.__gamesession.response[3]
                    i3, j3, k3 = self.__gamesession.response[4]
                    self.__client.send((''.join(str(e) for e in [code, player_id, i1, j1, k1, i2, j2, k2, i3, j3, k3]))
                                       .encode())
                if code == 'RST':
                    print('RST')
                    self.__client.send(b'RST')
                if code == 'QUT':
                    print('QUT')
                    self.__client.send(b'QUT')
                    # if self.player_id == player_id:
                    self.__client.shutdown(socket.SHUT_RDWR)
                    self.__client.close()
                    client_open = False
                self.__gamesession.set_semaphore()
