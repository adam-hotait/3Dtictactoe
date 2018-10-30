import numpy as np


class Board:
    """"
    This class is the 3D tic-tac-toe board.
    It stores the board states and checks for winning positions.
    """

    def __init__(self):
        self.__board = np.zeros((3, 3, 3), dtype=int)  # An empty board is created
        self.__win = False

    def reset(self):
        self.__init__()  # We reset the attributes when a reset is asked for

    @property
    def win(self):
        return self.__win

    def set_token(self, i, j, k, player_id):
        if self.__board[i][j][k] != 0:
            return 'ERR', 'NoToken'
        else:
            # Checking for winning position before adding token on board to prevent zero division
            response = self.check_for_win_pos(i, j, k, player_id)
            self.__board[i][j][k] = player_id
            return Board.format_response(response)

    def check_for_win_pos(self, i, j, k, player_id):
        """
        This function checks for a winning position by doing a scalar product of all vectors whose origin is the new
        token and extremity is an already present token from the same player
        :param i: Coordinate in x dimension
        :param j: Coordinate in y dimension
        :param k: Coordinate in z dimension
        :param player_id: Player who as put the token
        :return:
         * If not a winning position : [False, [i, j, k]]
         * If winning position : [True, [i1, j1, k1], [i2, j2, k2], [i3, j3, k3]] where i,j,k are coordinates of the
         three winning cubes.
        """
        new_token = np.array([i, j, k])
        vectors = (np.argwhere(self.__board == player_id)) - new_token
        for a in range(0, len(vectors)):
            for b in range(a + 1, len(vectors)):
                scalar_product = np.dot(vectors[a], vectors[b]) \
                                 / (np.linalg.norm(vectors[a], 2) * np.linalg.norm(vectors[b], 2))
                if np.isclose(scalar_product, 1) or np.isclose(scalar_product, -1):
                    self.__win = True
                    return [True, new_token, vectors[a] + new_token, vectors[b] + new_token]
        return [False, new_token]

    @staticmethod
    def format_response(response):
        if response[0]:  # if board has a winning position
            return 'WIN', response[1:]
        else:
            return 'SET', response[1:]


if __name__ == "__main__":
    board = Board()
    board.set_token(1, 1, 1, 1)
    board.set_token(0, 0, 0, 2)
    board.set_token(1, 0, 1, 1)
    board.set_token(1, 2, 1, 2)
    board.set_token(1, 0, 0, 1)
    board.set_token(1, 0, 2, 2)
    board.set_token(1, 2, 2, 1)
