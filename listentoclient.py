import threading


class ListenToClient(threading.Thread):
    def __init__(self, client, address, gamesession):
        super().__init__()
        print('init')
        self.client = client
        self.gamesession = gamesession
        self.size = 1024

    def run(self):
        print('ran')
        while True:
            try:
                data = self.client.recv(self.size)
                if data:
                    self.gamesession.receive_event(data)
                else:
                    raise ('Client disconnected')
            except:
                self.client.close()
                return False
