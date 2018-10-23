import threading


class SendToClient(threading.Thread):
    def __init__(self, client, gamesession):
        super().__init__()
        print('init')
        self.client = client
        self.gamesession = gamesession
        self.size = 1024

    def run(self):
        print('ran')
        while True:
            with self.gamesession.send_condition:
                self.gamesession.send_condition.wait()
                code = self.gamesession.response[0]
                player_id = self.gamesession.response[1]
                if code == 'SET':
                    i, j, k = self.gamesession.response[2]
                    self.client.send("{}{}{}{}{}".format(code, player_id, i, j, k).encode())
                if code == 'WIN':
                    i1, j1, k1 = self.gamesession.response[2]
                    i2, j2, k2 = self.gamesession.response[3]
                    i3, j3, k3 = self.gamesession.response[4]
                    self.client.send("{}{}{}{}{}{}{}{}{}{}{}".format(code, player_id, i1, j1, k1, i2, j2, k2, i3, j3, k3).encode())
                code = self.gamesession.response[0]
                self.gamesession.set_semaphore()


