import pygame
from graphical.colors import *


class MenuOption(pygame.sprite.Sprite):

    def __init__(self, text, option_text, position, size, text_color = WHITE, rectangle_color = BLACK,
                 selected_color = GREEN, font=None):
        pygame.sprite.Sprite.__init__(self)

        self.__text = text
        self.__return_text = option_text
        if font:
            self.__font = font
        else:
            self.__font = pygame.font.SysFont("comicsansms", 20)
        self.__position = position
        self.__size = size
        self.__text_color = text_color
        self.__rectangle_color = rectangle_color
        self.__rectangle_color_when_selected = selected_color

        # Sprite calculation
        self.__text_object = self.__font.render(self.__text, True, self.__text_color)
        self.__rect_object = pygame.Rect(self.__position[0], self.__position[1], self.__size[0], self.__size[1])
        text_w = self.__text_object.get_width()
        text_h = self.__text_object.get_height()
        self.__text_position = self.__position[0] + (self.__size[0] - text_w) / 2, self.__position[1] + (
                self.__size[1] - text_h) / 2

    @property
    def return_text(self):
        """Returns the otion code"""
        return self.__return_text

    def update(self):
        # Sprite calculation
        self.__text_object = self.__font.render(self.__text, True, self.__text_color)
        self.__rect_object = pygame.Rect(self.__position[0], self.__position[1], self.__size[0], self.__size[1])
        text_w = self.__text_object.get_width()
        text_h = self.__text_object.get_height()
        self.__text_position = self.__position[0] + (self.__size[0] - text_w) / 2, self.__position[1] + (
                self.__size[1] - text_h) / 2

    def draw(self, screen, is_selected):

        self.update()

        if is_selected:
            color = self.__rectangle_color_when_selected
        else:
            color = self.__rectangle_color

        pygame.draw.rect(screen, color, self.__rect_object)
        screen.blit(self.__text_object, self.__text_position)

    def point_in_rectangle(self, point):

        if point[0] >= self.__position[0] and point[1] >= self.__position[1] and point[0] <= self.__position[0] + self.__size[
            0] and point[1] <= self.__position[1] + self.__size[1]:
            return True
        else:
            return False
