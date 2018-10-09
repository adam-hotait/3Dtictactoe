import pygame
from pygame.locals import *
from graphical.clientSideBoard import ClientSideBoard


class Gui3D():
    
    def __init__(self, commObject, window):

        self.__screen = window.screen
        
        
        self.__commObject = commObject
        
        self.__board = ClientSideBoard()
        
        self.__board.size = window.get_dimension()
        self.__board.position = 0, 0
        
        self.__board.generate()
        
        
        self.rotation_speed = 0.5 #Speed at which the grid turns when an arrow is pressed, in rad/s

        
    def reset_board(self):
        self.__board.reset()
    
    def set_token(self, i, j, k, token):
        self.__board.set_token(i, j, k, token)
    
    def run(self):
        
        
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
            
            
            #Now we take care of the grid rotation
            new_timer = pygame.time.get_ticks()
            elapsed = (new_timer - timer) / 1000
            timer = new_timer
            if arrow_up:
                self.__board.view.rotate(0, self.rotation_speed * elapsed)
            if arrow_down:
                self.__board.view.rotate(0, -self.rotation_speed * elapsed)
            if arrow_left:
                self.__board.view.rotate(1, -self.rotation_speed * elapsed)
            if arrow_right:
                self.__board.view.rotate(1, self.rotation_speed * elapsed) 
            
            #Now we draw everything
            
            self.__screen.fill((0, 0, 0))
            self.__board.draw(self.__screen, selected=selected_cube)
            pygame.display.flip()
            clock.tick(60)
    
    def close(self):
        pygame.quit()
        
        
        
        