import pygame
from client_side.graphical.colors import *
from client_side.graphical.menuOption import MenuOption
import re


class InputAddress(pygame.sprite.Sprite):
    """Pop-up window for IP address input"""

    def __init__(self, position, size):
        """Constructor"""
        pygame.sprite.Sprite.__init__(self)
        self.__position = position
        self.__size = size
        self.__text_color = WHITE
        self.__rectangle_color = BLUE
        self.__button_color = RED
        self.__input_back_color = BLACK
        self.__display_text = "Please enter the server IP, or click localhost"
        self.__input_text = " "
        self.__font = pygame.font.SysFont("comicsansms", 12)

        #Generation of the elements of the window

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
        size_ok = (
            int(self.__size[0] / 2),
            int(self.__size[0] / 15))
        position_ok = (
            int(self.__position[0] + (self.__size[0] - size_ok[0]) / 2),
            int(self.__input_rect.y + self.__input_rect.h + (1 / 20) * self.__size[1]))
        self.__ok_button = MenuOption("Ok", "OK", position_ok, size_ok, font=self.__font)

        # Localhost button
        size_lh = (
            int(self.__size[0] / 2),
            int(self.__size[0] / 15))
        position_lh = (
            int(self.__position[0] + (self.__size[0] - size_lh[0]) / 2),
            int(position_ok[1] + size_ok[1] + (1 / 20) * self.__size[1]))
        self.__lh_button = MenuOption("Localhost", "LH", position_lh, size_lh, font=self.__font)

        # Quit button
        size_qut = (
            int(self.__size[0] / 2),
            int(self.__size[0] / 15))
        position_qut = (
            int(self.__position[0] + (self.__size[0] - size_qut[0]) / 2),
            int((self.__size[1] + size_lh[1] + position_lh[1] - self.__position[1] -
                 size_qut[1]) / 2))
        self.__quit_button = MenuOption("Return", "RETURN", position_qut, size_qut, font=self.__font)

        self.__buttons = [self.__ok_button, self.__lh_button, self.__quit_button]

        #Not-an-IP text
        self.__not_ip_object = self.__font.render("This does not look like an IP", True, self.__text_color)
        self.__not_ip_position = int(
            self.__position[0] + (self.__size[0] - self.__not_ip_object.get_width()) / 2), int(
            self.__position[1] + (25 / 30) * self.__size[1])

    def __update(self):
        """Updates the input text object"""
        self.__input_text_object = self.__font.render(self.__input_text, True, self.__text_color)
        self.__input_text_position = (
            int(self.__input_rect.x + (self.__input_rect.w - self.__input_text_object.get_width()) / 2),
            int(self.__input_rect.y + (self.__input_rect.h - self.__input_text_object.get_height()) / 2))

    def addChar(self, char):
        """Adds a character to the input text"""
        self.__input_text += char
        self.__update()

    def removeChar(self):
        """Removes a character from the input text"""
        self.__input_text = self.__input_text[:-1]
        if len(self.__input_text) == 0:
            self.__input_text = " "
        self.__update()

    def get_input_text(self):
        """Returns the input text"""
        return self.__input_text.strip()

    def get_number_buttons(self):
        """Returns the number of buttons"""
        return len(self.__buttons)

    def get_button_mesage_from_index(self, index):
        """Returns the message of a button from its index"""
        return self.__buttons[index].return_text

    def cursor_on_button(self, click_pos):
        """Return on which button the cursor is"""

        for k in range(len(self.__buttons)):
            button = self.__buttons[k]
            if button.point_in_rectangle(click_pos):
                return k
        return -1

    def __valid_ip(self):
        """Tells if the input text is a valid IP"""
        return not (self.__input_text.strip().upper() != "LOCALHOST" and not re.match('^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)[.]'
                                                   + '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)[.]'
                                                   + '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)[.]'
                                                   + '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', self.__input_text.strip()))

    def draw(self, screen, selected_button):
        """Draws the pop-up window"""

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
        if not self.__valid_ip():
            screen.blit(self.__not_ip_object, self.__not_ip_position)
