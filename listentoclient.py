import threading
import socket


class ListenToClient(threading.Thread):
    """
    This class receives messages from the client.
    There is one dedicated instance per client.
    """
    def __init__(self, client, game_session, player_id):
        super().__init__()
        print('init')
        self.__client = client
        self.__game_session = game_session
        self.__player_id = player_id

    def run(self):
        client_open = True
        while client_open:
            try:
                data = self.__client.recv(1024)
                if data:
                    print('recv client: ', data)
                    data = data.decode()
                    data_dict = dict(player_id=self.__player_id)
                    data_dict["command"] = data[0:3]
                    if data_dict["command"] == 'CLK':  # Simple formatting of the received command
                        data_dict["i"] = int(data[3])
                        data_dict["j"] = int(data[4])
                        data_dict["k"] = int(data[5])
                    self.__game_session.receive_event(data_dict)
            except socket.error:
                print("Player {} disconnected".format(self.__player_id))
                client_open = False
