import threading
import socket

class SendToClient(threading.Thread):
    def __init__(self, client, gamesession, player_id):
        super().__init__()
        print('init')
        self.client = client
        self.gamesession = gamesession
        self.size = 1024
        self.player_id = player_id

    def run(self):
        client_open = True
        self.client.send(b'NEW')
        while client_open:
            with self.gamesession.send_condition:
                self.gamesession.send_condition.wait()
                code = self.gamesession.response[0]
                player_id = self.gamesession.response[1]
                if code == 'SET':
                    i, j, k = self.gamesession.response[2]
                    self.client.send((''.join(str(e) for e in [code, player_id, i, j, k])).encode())
                if code == 'WIN':
                    i1, j1, k1 = self.gamesession.response[2]
                    i2, j2, k2 = self.gamesession.response[3]
                    i3, j3, k3 = self.gamesession.response[4]
                    self.client.send((''.join(str(e) for e in [code, player_id, i1, j1, k1, i2, j2, k2, i3, j3, k3]))
                                     .encode())
                if code == 'QUT':
                    print('QUT')
                    self.client.send(b'QUT')
                    # if self.player_id == player_id:
                    self.client.shutdown(socket.SHUT_RDWR)
                    self.client.close()
                    client_open = False
                self.gamesession.set_semaphore()


