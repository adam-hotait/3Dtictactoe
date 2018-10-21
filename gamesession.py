import threading
from board import Board


class GameSession(threading.Thread):
    def __init__(self):
        print('session')
        threading.Thread.__init__(self)
        self.__playerlist = []
        self.__data_queue = []
        self.__response = None
        self.__current_player = 0
        self.__board = Board()
        self.__recvEvent = threading.Event()
        self.__sendCondition = threading.Condition()
        self.__lock = threading.RLock()
        self.__semaphore = threading.BoundedSemaphore(2)

    @property
    def response(self):
        return self.__response

    @property
    def send_condition(self):
        return self.__sendCondition

    def receive_event(self, data):
        with self.__lock:
            self.__data_queue.append(data)
            self.__recvEvent.set()

    def set_semaphore(self):
        self.__semaphore.release()

    def run(self):
        while True:
            self.__recvEvent.wait()
            with self.send_condition:
                self.__semaphore.acquire()
                self.__semaphore.acquire()
                self.__response = None
                with self.__lock:
                    data_dict = self.__data_queue.pop()
                if not self.__board.win:
                    if data_dict['command'] == 'CLK':
                        if data_dict['player_id'] == self.__current_player:
                            status, token_data = self.__board.set_token(data_dict['i'], data_dict['j'], data_dict['k'],
                                                                        data_dict['player_id'])
                            if status == 'WIN':
                                self.__response = status, data_dict['player_id'], token_data[0], token_data[1], token_data[2]
                            else:
                                self.__response = status, data_dict['player_id'], token_data[0]
                else:
                    if data_dict['command'] == 'RST':
                        self.__board.reset()
                        self.__response = 'RST'
                if self.__response is not None:
                    with self.__lock:
                        self.__data_queue = []
                        self.__recvEvent.clear()
                    self.__sendCondition.notify_all()

    def newplayer(self, player):
        self.__playerlist.append(player)
        print(self.__playerlist)
