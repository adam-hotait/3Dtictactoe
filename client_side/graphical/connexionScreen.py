from .colors import *
import pygame
from pygame.locals import *
import socket
import select


class ConnexionScreen:
    """This class represent the waiting screen where the players must wait the other is ready"""

    def __init__(self, window, mySocket, isInviting=False):
        """Creates the connexion screen"""

        self.__window = window
        self.__socket = mySocket
        self.__back_color = BLUE
        self.__rect_color = RED
        self.__text_color = GREEN
        self.__isInviting = isInviting

        # Find our IP
        if isInviting:
            self.__ip = self.get_ip()

        w, h = window.get_dimension()
        rect_w = 500
        rect_h = 300

        self.__rectangle = pygame.rect.Rect(int((w - rect_w) / 2), int((h - rect_h) / 2), rect_w, rect_h)
        self.__font = pygame.font.SysFont("comicsansms", 20)
        if isInviting and not self.__ip == "127.0.0.1":
            self.__text_lines = [
                "Waiting for the other player...",
                "Your IP is: " + self.__ip,
                "Press Escape to go back"
            ]
        elif isInviting:
            self.__text_lines = [
                "Waiting for the other player...",
                "No connection found, use localhost.",
                "Press Escape to go back"
            ]
        else:
            self.__text_lines = [
                "Waiting for the server to accept",
                "Press Escape to go back"
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

    def get_ip(self):
        """Finds this client's IP"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

    def launch(self):
        """Launches the connexion screen"""
        print("go")
        running = True
        clock = pygame.time.Clock()

        while running:
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "QUT"
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return "MEN"

            # Waiting for a message from server
            socket_ready, _, _ = select.select([self.__socket], [], [], 0)
            if len(socket_ready) > 0:
                resp = self.__socket.recv(3)
                if resp:
                    response = resp.decode()
                    if response == "NEW":
                        return "NEW"
                    elif response == "QUT":
                        return "MEN"  # Return to menu (rather than quitting)

            # Drawing
            self.__window.screen.fill(self.__back_color)
            pygame.draw.rect(self.__window.screen, self.__rect_color, self.__rectangle)
            for k in range(len(self.__text_objects)):
                self.__window.screen.blit(self.__text_objects[k], self.__text_lines_positions[k])
                pygame.display.flip()
            clock.tick(60)
