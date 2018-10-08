import pygame
from pygame.locals import *
from menuOption import MenuOption
from inputAddress import InputAddress
from colors import *

class Menu():
    """Main menu of our game"""
    
    def __init__(self, window):
        
        self.__window = window
        
        w, h = window.get_dimension()  #width and height of the window
        
        #Creation of the menu options
        
        #Join option
        join_option = MenuOption()
        join_option.text = "Join Server"
        join_option.return_text = "JOIN"
        join_option.position = int((3/4)*w), int((1/20)*h)
        join_option.size = int((1/6)*w), int((1/20)*h)
        
        #Create option
        create_option = MenuOption()
        create_option.text = "Create Server"
        create_option.return_text = "CREATE"
        create_option.position = int((3/4)*w), int((2.5/20)*h)
        create_option.size = int((1/6)*w), int((1/20)*h)
        
        #Quit option
        quit_option = MenuOption()
        quit_option.text = "Quit"
        quit_option.return_text = "QUIT"
        quit_option.position = int((3/4)*w), int((4/20)*h)
        quit_option.size = int((1/6)*w), int((1/20)*h)
        

        
        self.__options = [join_option, create_option, quit_option]
            
    
        self.server_address = None
        
        
    def __get_selected_rectangle(self, pos):
        """Returns the rectangle which contains the point pos = (posx, posy). Returns -1 if no rectangle contains it."""
        for k in range(len(self.__options)):
            if self.__options[k].point_in_rectangle(pos):
                return k
        
        return -1
    
    
    
    def get_choice(self):
    
        choice_not_done = True
        
        while choice_not_done:
        
            running = True
            clock = pygame.time.Clock()
        
            selected_rect = -1 #index of the selected rectangle, -1 if no rectangle is selected
        
            clicked = None
        
            while running:
            
                for event in self.__window.get_events():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return "QUIT"
                    elif event.type == MOUSEMOTION:
                        new_selected_button = self.__get_selected_rectangle(event.pos)
                        if new_selected_button > -1:
                            selected_rect = new_selected_button
                    elif event.type == MOUSEBUTTONUP and event.button == 1:
                        clicked = self.__get_selected_rectangle(event.pos)
                        if clicked > -1:
                            running = False
                    elif event.type == KEYDOWN and event.key == K_UP:
                        if selected_rect == -1:
                            selected_rect = 0
                        elif selected_rect == 0:
                            selected_rect = len(self.__options) - 1
                        else:
                            selected_rect -= 1
                    elif event.type == KEYDOWN and event.key == K_DOWN:
                        if selected_rect == -1:
                            selected_rect = 0
                        elif selected_rect == len(self.__options) - 1:
                            selected_rect = 0
                        else:
                            selected_rect += 1
                    elif event.type == KEYDOWN and event.key == K_RETURN:
                        if selected_rect > -1:
                            clicked = selected_rect
                            running = False
                
                #Display
                self.__window.screen.fill((0, 0, 0))
            
                for k in range(len(self.__options)):
                    option = self.__options[k]
                
                    if k == selected_rect :
                        option.draw(self.__window.screen, True)
                    else:
                        option.draw(self.__window.screen, False)
            
                pygame.display.flip()
                clock.tick(60)
        
            #Now a button has been clicked on. If it is the "join server" button, we must ask the server address
            clicked_option = self.__options[clicked]
            if clicked_option.return_text == "JOIN":
                
                w, h = self.__window.get_dimension()
                
                inputBox = InputAddress()
                inputBox.position = (
                            int((1/3)*w),
                            int((1/20)*h))
                inputBox.size = (
                            int((w - inputBox.position[0]) / 2),
                            int((h - inputBox.position[1]) / 2))
                inputBox.generate()
                
                selected_rect = -1
            
                ip_entered = False
                go_back_to_menu = False
            
                clicked = None
                clock2 = pygame.time.Clock()
            
                while (not ip_entered) and (not go_back_to_menu):
                    for event in self.__window.get_events():
                        if event.type == QUIT:
                            return 'QUIT'
                        elif event.type == KEYDOWN and event.key == K_ESCAPE:
                            go_back_to_menu = True
                        elif event.type == MOUSEMOTION:
                            new_selected_button = inputBox.cursor_on_button(event.pos)
                            if new_selected_button > -1:
                                selected_rect = new_selected_button
                        elif event.type == MOUSEBUTTONUP and event.button == 1:
                            clicked = inputBox.cursor_on_button(event.pos)
                            if clicked > -1:
                                #A button has been clicked on
                                return_text = inputBox.get_button_mesage_from_index(clicked)
                                if return_text == "RETURN":
                                    go_back_to_menu = True
                                elif return_text == "LH":
                                    self.server_address = "127.0.0.1"
                                    ip_entered = True
                                elif return_text == "OK":
                                    self.server_address = inputBox.get_input_text()
                                    ip_entered = True
                    
                        elif event.type == KEYDOWN and event.key == K_UP:
                            if selected_rect == -1:
                                selected_rect = 0
                            elif selected_rect == 0:
                                selected_rect = inputBox.get_number_buttons() - 1
                            else:
                                selected_rect -= 1
                        elif event.type == KEYDOWN and event.key == K_DOWN:
                            if selected_rect == -1:
                                selected_rect = 0
                            elif selected_rect == inputBox.get_number_buttons() - 1:
                                selected_rect = 0
                            else:
                                selected_rect += 1
                        elif event.type == KEYDOWN and event.key == K_RETURN:
                            if selected_rect > -1:
                                #A button has been selected and entered
                                return_text = inputBox.get_button_mesage_from_index(selected_rect)
                                if return_text == "RETURN":
                                    go_back_to_menu = True
                                elif return_text == "LH":
                                    self.server_address = "127.0.0.1"
                                    ip_entered = True
                                elif return_text == "OK":
                                    self.server_address = inputBox.get_input_text()
                                    ip_entered = True
                            else:
                                self.server_address = inputBox.get_input_text()
                                ip_entered = True
                        
                        elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                            inputBox.removeChar()
                        elif event.type == KEYDOWN:
                            inputBox.addChar(event.unicode)
                        
                        
                        
                        
                        
                    #Display
                    self.__window.screen.fill((0, 0, 0))
                    for k in range(len(self.__options)):
                        option = self.__options[k]
                        option.draw(self.__window.screen, False)
                    inputBox.draw(self.__window.screen, selected_rect)
                    pygame.display.flip()
                    clock2.tick(60)
                #If an IP has been entered, we can stop this function here, else we do it again
                if ip_entered:
                    return "JOIN"
        
        
            #If the clicked button was not "join":
            else:
                return clicked_option.return_text

        
            
                    
        
        