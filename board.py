import numpy as np


class Board:
    """This class is the 3D tic-tac-toe board."""

    def __init__(self):
        self.board = np.zeros((3, 3, 3), dtype=int)
        self.__win = False

    def reset(self):
        self.__init__()

    @property
    def win(self):
        return self.__win

    def set_token(self, i, j, k, player_id):
        if self.board[i][j][k] != 0:
            raise Exception("Occupied space")
        else:
            # Checking for winning position before adding token on board to prevent zero division
            response = self.check_for_win_pos(i, j, k, player_id)
            self.board[i][j][k] = player_id
            return Board.format_response(response)

    def check_for_win_pos(self, i, j, k, player_id):
        new_token = np.array([i, j, k])
        vectors = (np.argwhere(self.board == player_id)) - new_token
        for a in range(0, len(vectors)):
            for b in range(a + 1, len(vectors)):
                scalar_product = np.dot(vectors[a], vectors[b]) \
                                 / (np.linalg.norm(vectors[a], 2) * np.linalg.norm(vectors[b], 2))
                if np.isclose(scalar_product, 1) or np.isclose(scalar_product, -1):
                    self.__win = True
                    return [True, new_token, vectors[a] + new_token, vectors[b] + new_token]
        return [False, new_token]

    # Maybe put it in a utilities class?
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
