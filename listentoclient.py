import threading


class ListenToClient(threading.Thread):
    def __init__(self, client, address, gamesession, player_id):
        super().__init__()
        print('init')
        self.client = client
        self.gamesession = gamesession
        self.size = 1024
        self.player_id = player_id

    def run(self):
        print('ran')
        while True:
            # try:
            data = self.client.recv(self.size)
            if data:
                data = data.decode()
                data_dict = dict(player_id = self.player_id)
                data_dict["command"] = data[0:3]
                if data_dict["command"] == 'CLK':
                    data["i"] = data[3]
                    data["j"] = data[4]
                    data["k"] = data[5]
                self.gamesession.receive_event(data)
            #     else:
            #         raise ('Client disconnected')
            # except:
            #     self.client.close()
            #     return False
