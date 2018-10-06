import numpy as np

class board:
    """Cette classe représente un plateau de jeu de morpion en 3D"""
	
	def __init__(self):
		self.board = np.zeros((3,3,3), dtype=int)
		
	def reset(self):
		self.__init__()
	
	def set_token(self, i, j, k, player_id):
		if self.board[i][j][k] != 0:
			raise Exception("Place déjà occupée")
		else:
			self.board[i][j][k] = player_id
	
	def verifier_gagnant(self, i, j, k):
		pass
		#TODO
		#Ligne qui a gagné : origine + vecteur