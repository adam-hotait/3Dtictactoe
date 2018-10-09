import pygame
from graphical.colors import *

class MenuOption(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.text = ""
        self.return_text = ""
        self.font = pygame.font.SysFont("comicsansms", 20)
        self.position = 0, 0
        self.size = 10, 10
        self.text_color = BLUE
        self.rectangle_color = RED
        self.rectangle_color_when_selected = GREEN
        
        #Sprite calculation
        self.__text_object = self.font.render(self.text, True, self.text_color)
        self.__rect_object = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        text_w = self.__text_object.get_width()
        text_h = self.__text_object.get_height()
        self.__text_position = self.position[0] + (self.size[0] - text_w)/2 , self.position[1] + (self.size[1] - text_h)/2
        
        
    
    def update(self):
        #Sprite calculation
        self.__text_object = self.font.render(self.text, True, self.text_color)
        self.__rect_object = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        text_w = self.__text_object.get_width()
        text_h = self.__text_object.get_height()
        self.__text_position = self.position[0] + (self.size[0] - text_w)/2 , self.position[1] + (self.size[1] - text_h)/2
    
    def draw(self, screen, is_selected):
    
        self.update()
        
        if is_selected:
            color = self.rectangle_color_when_selected
        else:
            color = self.rectangle_color
        
        pygame.draw.rect(screen, color, self.__rect_object)
        screen.blit(self.__text_object, self.__text_position)
    
    def point_in_rectangle(self, point):
        
        if point[0] >= self.position[0] and point[1] >= self.position[1] and point[0] <= self.position[0] + self.size[0] and point[1] <= self.position[1] + self.size[1]:
            return True
        else:
            return False
        