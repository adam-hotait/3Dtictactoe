import threading
import socket

class ListenToClient(threading.Thread):
    def __init__(self, client, gamesession, player_id):
        super().__init__()
        print('init')
        self.client = client
        self.gamesession = gamesession
        self.size = 1024
        self.player_id = player_id

    def run(self):
        client_open = True
        while client_open:
            try:
                data = self.client.recv(self.size)
                if data:
                    print('recv client: ', data)
                    data = data.decode()
                    data_dict = dict(player_id = self.player_id)
                    data_dict["command"] = data[0:3]
                    if data_dict["command"] == 'CLK':
                        data_dict["i"] = int(data[3])
                        data_dict["j"] = int(data[4])
                        data_dict["k"] = int(data[5])
                    self.gamesession.receive_event(data_dict)
            #     else:
            #         raise ('Client disconnected')
            except socket.error as msg:
                print("disconnected :", msg)
                client_open = False
