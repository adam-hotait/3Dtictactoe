import pygame
from pygame.locals import *

class window:
	"""This class will be the main window of our program, it will display menus and the Tic Tac Toe board"""
	
	def __init__(self, window_dimension):
		"""Initialization of some variables, creating the window"""
		pygame.init()
		pygame.display.set_caption("Tic Tac Toe")
		
		
		self.__screen = pygame.display.set_mode(window_dimension)
	
	def get_events(self):
		"""Returns events in the queue"""
		pygame.event.get()
	
	def close(self):
		pygame.display.quit()
		pygame.quit()
		
		
		
		
