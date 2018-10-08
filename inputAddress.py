import pygame
from pygame.locals import *
from colors import *
from menuOption import MenuOption

class InputAddress(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.position = 0, 0
        
        self.size = 100, 100
        
        self.text_color = WHITE
        
        self.rectangle_color = BLUE
        
        self.button_color = RED
        
        self.input_back_color = BLACK
        
        self.display_text = "Please enter the server IP, or click localhost"
        
        self.__input_text = " "
        
        self.font = pygame.font.SysFont("comicsansms", 15)
    
    def generate(self):
        
        #Big rectangle of the input box
        self.__big_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        
        #Display text object
        self.__display_text_object = self.font.render(self.display_text, True, self.text_color)
        self.__display_text_position = int(self.position[0] + (self.size[0] - self.__display_text_object.get_width()) / 2), int(self.position[1] + (1/30) * self.size[1])
        
        #Input text rectangle
        self.__input_rect = pygame.Rect(
                    int(self.position[0] + (1/20) * self.size[0]),
                    int(self.__display_text_position[1] + self.__display_text_object.get_height() + (1/30) * self.size[1]),
                    int(self.size[0] * 9/10),
                    int(self.size[1] * 1/10))
        
        #Input text object
        self.__input_text_object = self.font.render(self.__input_text, True, self.text_color)
        self.__input_text_position = (
                    int(self.__input_rect.x + (self.__input_rect.w - self.__input_text_object.get_width()) / 2),
                    int(self.__input_rect.y + (self.__input_rect.h - self.__input_text_object.get_height()) / 2))
        
        #Ok button
        self.__ok_button = MenuOption()
        self.__ok_button.text = "Ok"
        self.__ok_button.return_text = "OK"
        self.__ok_button.font = self.font
        self.__ok_button.size = (
                    int(self.size[0] / 2),
                    int(self.size[0] / 15))
        self.__ok_button.position = (
                    int(self.position[0] + (self.size[0] - self.__ok_button.size[0]) / 2),
                    int(self.__input_rect.y + self.__input_rect.h + (1/20) * self.size[1]))
        
        #Localhost button
        self.__lh_button = MenuOption()
        self.__lh_button.text = "Localhost"
        self.__lh_button.return_text = "LH"
        self.__lh_button.font = self.font
        self.__lh_button.size = (
                    int(self.size[0] / 2),
                    int(self.size[0] / 15))
        self.__lh_button.position = (
                    int(self.position[0] + (self.size[0] - self.__lh_button.size[0]) / 2),
                    int(self.__ok_button.position[1] + self.__ok_button.size[1] + (1/20) * self.size[1]))
        
        #Quit button
        self.__quit_button = MenuOption()
        self.__quit_button.text = "Return"
        self.__quit_button.return_text = "RETURN"
        self.__quit_button.font = self.font
        self.__quit_button.size = (
                    int(self.size[0] / 2),
                    int(self.size[0] / 15))
        self.__quit_button.position = (
                    int(self.position[0] + (self.size[0] - self.__quit_button.size[0]) / 2),
                    int((self.size[1] + self.__lh_button.size[1] + self.__lh_button.position[1] - self.position[1] - self.__quit_button.size[1]) / 2))
    
        self.__buttons = [self.__ok_button, self.__lh_button, self.__quit_button]
        
        
        
    def __update(self):
        self.__input_text_object = self.font.render(self.__input_text, True, self.text_color)
        self.__input_text_position = (
                    int(self.__input_rect.x + (self.__input_rect.w - self.__input_text_object.get_width()) / 2),
                    int(self.__input_rect.y + (self.__input_rect.h - self.__input_text_object.get_height()) / 2))
    
    def addChar(self, char):
        self.__input_text += char
        self.__update()
    
    def removeChar(self):
        self.__input_text = self.__input_text[:-1]
        if len(self.__input_text) == 0:
            self.__input_text = " "
        self.__update()
    
    def get_input_text(self):
        return self.__input_text
    
    def get_number_buttons(self):
        return len(self.__buttons)
    
    def get_button_mesage_from_index(self, index):
        return self.__buttons[index].return_text
    
    def cursor_on_button(self, click_pos):
        
        for k in range(len(self.__buttons)):
            button = self.__buttons[k]
            if button.point_in_rectangle(click_pos):
                return k
        return -1
    
    def draw(self, screen, selected_button):
        
        pygame.draw.rect(screen, self.rectangle_color, self.__big_rect)
        screen.blit(self.__display_text_object, self.__display_text_position)
        
        pygame.draw.rect(screen, self.input_back_color, self.__input_rect)
        screen.blit(self.__input_text_object, self.__input_text_position)
        
        for k in range(len(self.__buttons)):
            button = self.__buttons[k]
            if k == selected_button:
                button.draw(screen, True)
            else:
                button.draw(screen, False)
                
    
    
        
        