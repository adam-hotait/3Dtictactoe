from .colors import *
import pygame
from pygame.locals import *


class DeconnectionScreen:
    """This class represent the waiting screen where the players must wait the other is ready"""

    def __init__(self, window):
        """Creates the connection screen"""

        self.__window = window
        self.__back_color = BLUE
        self.__rect_color = RED
        self.__text_color = GREEN

        w, h = window.get_dimension()
        rect_w = 500
        rect_h = 300

        self.__rectangle = pygame.rect.Rect(int((w - rect_w)/2), int((h - rect_h)/2), rect_w, rect_h)
        self.__font = pygame.font.SysFont("comicsansms", 20)
        self.__text_lines = [
            "Connexion error",
            "Return to menu in 5 seconds",
            "(Press Escape if you are in a hurry)"
        ]

        # Creation of the text objects
        lines = len(self.__text_lines)
        self.__text_objects = [self.__font.render(line, True, self.__text_color) for line in self.__text_lines]
        self.__text_lines_positions = []
        last_y_pos = 0
        line_height = self.__text_objects[0].get_height()
        for k in range(lines):
            text_obj = self.__text_objects[k]
            width, height = text_obj.get_width(), text_obj.get_height()
            position_x = self.__rectangle.x + int((self.__rectangle.w - width) / 2)
            position_y = self.__rectangle.y + last_y_pos + 10 + line_height + 10
            last_y_pos += line_height + 20
            self.__text_lines_positions.append((position_x, position_y))

    def launch(self):
        """Launches the connexion screen"""
        print("go")
        clock = pygame.time.Clock()
        init_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - init_time < 5000:
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "QUT"
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return "MEN"

            # Drawing
            self.__window.screen.fill(self.__back_color)
            pygame.draw.rect(self.__window.screen, self.__rect_color, self.__rectangle)
            for k in range(len(self.__text_objects)):
                self.__window.screen.blit(self.__text_objects[k], self.__text_lines_positions[k])
                pygame.display.flip()
            clock.tick(60)
        return "MEN"

