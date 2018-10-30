import threading
from .board import Board


class GameSession(threading.Thread):
    """
    Game session thread.
    This thread orchestrates the game once two players have joined the server.
    """
    def __init__(self):
        # The game session is running in its own thread
        threading.Thread.__init__(self)

        # The following objects and variables are where messages are stored
        self.__data_queue = []  # List storing all received messages
        self.__response = None  # Variable storing the message that should be send to players

        # The following objects and variables are storing the game state
        self.__current_player = 1
        self.__board = Board()  # The Board object instance stores the state of the board

        # The following variable that stores the running state of the game session thread
        self.__running = True

        # The following threading objects are in charge of coordination between the game session
        # and the 'SendToClient' and 'ListenToClient' threads.
        #
        # This is a simple lock to prevents concurrent access to ressources
        self.__lock = threading.RLock()
        #
        # This event will be set when if a player has performed an action
        self.__recvEvent = threading.Event()
        #
        # This condition will be used to notify 'SendToClient' threads that there is a response for them to send
        self.__sendCondition = threading.Condition()
        #
        # This semaphore will be used to make sure that both 'SendToClient' threads send response before performing
        # another action
        self.__semaphore = threading.BoundedSemaphore(2)

        print('Game session created')

    @property
    def response(self):
        return self.__response

    @property
    def send_condition(self):
        return self.__sendCondition

    @property
    def current_player(self):
        return str(self.__current_player)

    def receive_event(self, data):
        with self.__lock:
            self.__data_queue.append(data)
            self.__recvEvent.set()

    def set_semaphore(self):
        self.__semaphore.release()

    def run(self):
        print('Game session started')
        while self.__running:
            self.__recvEvent.wait()  # Wait for a message incoming from a player
            with self.send_condition:
                self.__semaphore.acquire()  # Make sure 'SendToClient' is not using __response
                self.__semaphore.acquire()  # Make sure the other 'SendToClient' is not using __response
                # NB: 2 semaphores are used instead of 1 lock so that clients can *simultaneously* send __response

                self.__response = None  # Response can be set to None as it was sent (both semaphores are acquired)
                with self.__lock:
                    data_dict = self.__data_queue.pop()  # We take the latest command received

                print('Now processing message: {}'.format(data_dict))
                # If the game hasn't been won, the command is a play on a cube and it is from the current player...
                # (NB: if it is not the current player's turn, the command will be ignored)
                if not self.__board.win and\
                        data_dict['command'] == 'CLK' and\
                        data_dict['player_id'] == self.__current_player:

                    # Try to insert the token in the board and store the returned data
                    status, token_data = self.__board.set_token(data_dict['i'], data_dict['j'], data_dict['k'],
                                                                data_dict['player_id'])
                    # If the board returns an error (because the played cube is already taken), do nothing
                    if status == 'ERR':
                        print('Cube already occupied')
                    # If the play is legit, store the returned data in __response
                    else:
                        if status == 'WIN':
                            self.__response = status, data_dict['player_id'], token_data[0], token_data[1], token_data[2]
                        else:
                            self.__response = status, data_dict['player_id'], token_data[0]
                        # Switch the current player
                        self.__current_player = (self.__current_player + 2) % 2 + 1

                # If the game is over and a new party has been requested, reset the game
                elif data_dict['command'] == 'RST':
                        self.__board.reset()
                        self.__response = 'RST', data_dict['player_id']

                # If a player quits the game, end the game session
                if data_dict['command'] == 'QUT':
                    self.__running = False
                    self.__response = 'QUT', data_dict['player_id']

                # At this point the received message has been processed, we can clear the receive event
                self.__recvEvent.clear()

                # If the command was legit, a response was set and we can notifiy the 'SendToClient' threads
                if self.__response is not None:
                    with self.__lock:
                        self.__data_queue = []
                    print('The command was legit. Now sending response: {}'.format(self.response))
                    self.__sendCondition.notify_all()
                else:
                    # If the response is None, it won't be used by 'SendToClient' threads, we can release the semaphores
                    print('The message {} was illegal. Discarding.'.format(data_dict))
                    self.__semaphore.release()
                    self.__semaphore.release()
        print('Game session exited.')

