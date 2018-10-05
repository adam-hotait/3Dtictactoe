#-*-coding:utf8-*-

class PlaceDejaOccupee(Exception):
	pass

class plateau:
	"""Cette classe représente un plateau de jeu de morpion en 3d"""
	
	def __init__(self):
		
		self.disposition = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		
	def reset(self):
		self.disposition = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
	
	def placer_jeton(self, i, j, k, joueur_id):
		
		if self.disposition[i][j][k] != 0:
			raise PlaceDejaOccupee ("Place déjà occupée")
		else:
			self.disposition[i][j][k] = joueur_id
	
	def verifier_gagnant(self, i, j, k):
		
		gagnant_potentiel = self.disposition[i][j][k]
		
		if self.disposition[0][j][k] == gagnant_potentiel and self.disposition[1][j][k] == gagnant_potentiel and self.disposition[2][j][k] == gagnant_potentiel:
			return gagnant_potentiel
		elif self.disposition[i][0][k] == gagnant_potentiel and self.disposition[i][1][k] == gagnant_potentiel and self.disposition[i][j][2] == gagnant_potentiel:
			pass
		#TODO
		#Ligne qui a gagné : origine + vecteur