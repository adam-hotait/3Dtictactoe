import pygame
from pygame.locals import *
from clientSideBoard import ClientSideBoard
import numpy as np
from colors import *


class Gui3D():
    """Class for all the 3D GUI of the TicTacToe"""
    
    def __init__(self, commObject, window):
        """Constructor. Default values of attributes (can be modified later)"""

        self.__window = window

        self.__screen = self.__window.screen
        
        
        self.__commObject = commObject
        
        self.__board = ClientSideBoard()
        
        self.__board.size = window.get_dimension()
        self.__board.position = 0, 0
        
        self.__board.generate()

        self.rotation_speed = 0.5 #Speed at which the grid turns when an arrow is pressed, in rad/s
        self.__rotation_when_won = 0.7

        # Font to display the winner's name
        self.__font = pygame.font.SysFont("comicsansms", 70)
        self.__text_object_winner_1 = self.__font.render("Player 1 Won !!!", True, RED_DARK)
        self.__text_object_winner_2 = self.__font.render("Player 2 Won !!!", True, BLUE_DARK)


        
    def reset_board(self):
        """Removes all tokens"""
        self.__board.reset()
    
    def set_token(self, i, j, k, token):
        """Sets a token in the (i, j, k) cube"""
        self.__board.set_token(i, j, k, token)
    
    def run(self):
        """Launches the GUI"""
        
        running = True
        clock = pygame.time.Clock()
        clock_tick = 60
        timer = pygame.time.get_ticks()
        
        #Keep in memory which arrow is pressed
        arrow_up = False
        arrow_down = False
        arrow_left = False
        arrow_right = False
        
        selected_cube = None
        
        winning_player = 0
        winning_line = []
        
        #Main Loop
        while running:
            
            #Events
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.__commObject.gui_add_event(["QUIT"])
                    running = False
                    
                elif event.type == KEYDOWN and event.key == K_UP:
                    arrow_up = True
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    arrow_down = True
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    arrow_left = True
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    arrow_right = True
                elif event.type == KEYUP and event.key == K_UP:
                    arrow_up = False
                elif event.type == KEYUP and event.key == K_DOWN:
                    arrow_down = False
                elif event.type == KEYUP and event.key == K_LEFT:
                    arrow_left = False
                elif event.type == KEYUP and event.key == K_RIGHT:
                    arrow_right = False
                
                elif event.type == MOUSEMOTION:
                    selected_cube = self.__board.point_on_a_cube(event.pos)
                
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    self.__commObject.gui_add_event(["CLICK", selected_cube])
                
            #Checking the commands the Main thread could have sent
            for event in self.__commObject.get_and_empty_Main_events():
                if event[0] == "QUIT":
                    running = False
                elif event[0] == "SET_TOKEN":
                    self.set_token(event[1], event[2], event[3], event[4])
                elif event[0] == "RESET":
                    self.reset_board()
                elif event[0] == "WIN":
                    winning_player = event[1]
                    winning_line = event[2]
                    self.__board.view.set_angles(2 * np.pi / 18, 2 * np.pi / 18)
            
            
            #Now we take care of the grid rotation
            new_timer = pygame.time.get_ticks()
            elapsed = (new_timer - timer) / 1000
            timer = new_timer
            if winning_player == 0:
                if arrow_up:
                    self.__board.view.rotate(0, self.rotation_speed * elapsed)
                if arrow_down:
                    self.__board.view.rotate(0, -self.rotation_speed * elapsed)
                if arrow_left:
                    self.__board.view.rotate(1, -self.rotation_speed * elapsed)
                if arrow_right:
                    self.__board.view.rotate(1, self.rotation_speed * elapsed)
            else:
                self.__board.view.rotate(1, self.__rotation_when_won * elapsed)
            
            #Now we draw everything
            
            self.__screen.fill((0, 0, 0))
            self.__board.draw(self.__screen, selected_cube, winning_player, winning_line)
            window_dim = self.__window.get_dimension()
            if winning_player == 1:
                text_dim = self.__text_object_winner_1.get_size()
                self.__screen.blit(
                    self.__text_object_winner_1,
                    (((window_dim[0] - text_dim[0]) / 2),
                    ((window_dim[1] - text_dim[1]) / 8)))
            elif winning_player == 2:
                text_dim = self.__text_object_winner_2.get_size()
                self.__screen.blit(
                    self.__text_object_winner_2,
                    (((window_dim[0] - text_dim[0]) / 2),
                     ((window_dim[1] - text_dim[1]) / 8)))

            pygame.display.flip()
            clock.tick(60)
        
        
        
        