import threading


class SendToClient(threading.Thread):
    def __init__(self, client, address, gamesession):
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

                self.gamesession.set_semaphore()


