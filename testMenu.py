from window import Window
from menu import Menu
import pygame
from pygame.locals import *

window = Window((1280, 720))

menu = Menu(window)

choice = menu.get_choice()

print("Vous avez choisi : ", choice)

if choice == 'JOIN':
    serv = menu.server_address
    
    print("Rejoindre serveur à l'adresse :", serv)
    
window.close()