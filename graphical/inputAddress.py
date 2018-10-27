import pygame
from graphical.colors import *
from graphical.menuOption import MenuOption


class InputAddress(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.__position = 0, 0
        self.__size = 100, 100
        self.__text_color = WHITE
        self.__rectangle_color = BLUE
        self.__button_color = RED
        self.__input_back_color = BLACK
        self.__display_text = "Please enter the server IP, or click localhost"
        self.__input_text = " "
        self.__font = pygame.font.SysFont("comicsansms", 15)

    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, xy):
        try:
            x, y = xy
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            """ This will run only if no exception was raised """
            self.__position = x, y

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, xy):
        try:
            x, y = xy
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            """ This will run only if no exception was raised """
            self.__size = x, y

    def generate(self):

        # Big rectangle of the input box
        self.__big_rect = pygame.Rect(self.__position[0], self.__position[1], self.__size[0], self.__size[1])

        # Display text object
        self.__display_text_object = self.__font.render(self.__display_text, True, self.__text_color)
        self.__display_text_position = int(
            self.__position[0] + (self.__size[0] - self.__display_text_object.get_width()) / 2), int(
            self.__position[1] + (1 / 30) * self.__size[1])

        # Input text rectangle
        self.__input_rect = pygame.Rect(
            int(self.__position[0] + (1 / 20) * self.__size[0]),
            int(self.__display_text_position[1] + self.__display_text_object.get_height() + (1 / 30) * self.__size[1]),
            int(self.__size[0] * 9 / 10),
            int(self.__size[1] * 1 / 10))

        # Input text object
        self.__input_text_object = self.__font.render(self.__input_text, True, self.__text_color)
        self.__input_text_position = (
            int(self.__input_rect.x + (self.__input_rect.w - self.__input_text_object.get_width()) / 2),
            int(self.__input_rect.y + (self.__input_rect.h - self.__input_text_object.get_height()) / 2))

        # Ok button
        self.__ok_button = MenuOption()
        self.__ok_button.text = "Ok"
        self.__ok_button.return_text = "OK"
        self.__ok_button.font = self.__font
        self.__ok_button.size = (
            int(self.__size[0] / 2),
            int(self.__size[0] / 15))
        self.__ok_button.position = (
            int(self.__position[0] + (self.__size[0] - self.__ok_button.size[0]) / 2),
            int(self.__input_rect.y + self.__input_rect.h + (1 / 20) * self.__size[1]))

        # Localhost button
        self.__lh_button = MenuOption()
        self.__lh_button.text = "Localhost"
        self.__lh_button.return_text = "LH"
        self.__lh_button.font = self.__font
        self.__lh_button.size = (
            int(self.__size[0] / 2),
            int(self.__size[0] / 15))
        self.__lh_button.position = (
            int(self.__position[0] + (self.__size[0] - self.__lh_button.size[0]) / 2),
            int(self.__ok_button.position[1] + self.__ok_button.size[1] + (1 / 20) * self.__size[1]))

        # Quit button
        self.__quit_button = MenuOption()
        self.__quit_button.text = "Return"
        self.__quit_button.return_text = "RETURN"
        self.__quit_button.font = self.__font
        self.__quit_button.size = (
            int(self.__size[0] / 2),
            int(self.__size[0] / 15))
        self.__quit_button.position = (
            int(self.__position[0] + (self.__size[0] - self.__quit_button.size[0]) / 2),
            int((self.__size[1] + self.__lh_button.size[1] + self.__lh_button.position[1] - self.__position[1] -
                 self.__quit_button.size[1]) / 2))

        self.__buttons = [self.__ok_button, self.__lh_button, self.__quit_button]

    def __update(self):
        self.__input_text_object = self.__font.render(self.__input_text, True, self.__text_color)
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

        pygame.draw.rect(screen, self.__rectangle_color, self.__big_rect)
        screen.blit(self.__display_text_object, self.__display_text_position)

        pygame.draw.rect(screen, self.__input_back_color, self.__input_rect)
        screen.blit(self.__input_text_object, self.__input_text_position)

        for k in range(len(self.__buttons)):
            button = self.__buttons[k]
            if k == selected_button:
                button.draw(screen, True)
            else:
                button.draw(screen, False)
