import numpy as np


class Board:
    """This class is the 3D tic-tac-toe board."""

    def __init__(self):
        self.board = np.zeros((3, 3, 3), dtype=int)

    def reset(self):
        self.__init__()

    def set_token(self, i, j, k, player_id):
        if self.board[i][j][k] != 0:
            raise Exception("Occupied space")
        else:
            self.check_for_win_pos(i, j, k, player_id)
            self.board[i][j][k] = player_id

    def check_for_win_pos(self, i, j, k, player_id):
        print('-' * 11 + 'new token' + '-' * 11)
        new_token = np.array([i, j, k])
        vectors = (np.argwhere(self.board == player_id)) - new_token
        print('Board')
        print(np.argwhere(self.board == player_id))
        print('vectors')
        print(vectors)
        print('-'*11+'dot'+'-'*11)
        for a in range(0, len(vectors)):
            for b in range(a+1, len(vectors)):
                scalar_product = np.dot(vectors[a], vectors[b])\
                                 / (np.linalg.norm(vectors[a], 2) * np.linalg.norm(vectors[b], 2))
                print(scalar_product, ' scalar product')
                print(vectors[a], ' a')
                print(vectors[b], 'b')
                if np.isclose(scalar_product, 1) or np.isclose(scalar_product, -1):
                    print('ok ', new_token, vectors[a] + new_token, vectors[b] + new_token)
                else:
                    print('no ', new_token)


if __name__ == "__main__":
    board = Board()
    board.set_token(1, 0, 1, 1)
    board.set_token(2, 0, 0, 1)
    board.set_token(2, 2, 0, 1)
    board.set_token(2, 1, 0, 1)
