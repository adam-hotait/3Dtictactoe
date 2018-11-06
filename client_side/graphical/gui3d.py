import pygame
from pygame.locals import *
from .clientSideBoard import ClientSideBoard
import numpy as np
from .colors import *
from .deconnectionScreen import DeconnectionScreen


class Gui3D:
    """Class for all the 3D GUI of the TicTacToe"""

    def __init__(self, comm_object, window, player, sound_object, comm_object2=None):
        """Constructor. Default values of attributes (can be modified later)"""

        self.__window = window
        self.__player = player  # 0 if local 2 player
        self.__sound_object = sound_object
        self.__commObject = comm_object
        self.__commObject2 = comm_object2  # Only useful in local 2 player
        self.__board = ClientSideBoard()
        self.__board.size = window.get_dimension()
        self.__board.position = 0, 0
        self.__board.generate()

        # Speed at which the grid turns
        self.__rotation_speed = 0.5  # When an arrow is pressed, in rad/s
        self.__rotation_speed_mouse = 0.01  # When the mouse is used
        self.__rotation_when_won = 0.7  # When the board auto-rotates after a win

        # Font to display the winner's name
        self.__font = pygame.font.SysFont("comicsansms", 70)
        self.__text_object_winner_1 = self.__font.render("Player 1 Won !!!", True, RED_DARK)
        self.__text_object_winner_2 = self.__font.render("Player 2 Won !!!", True, BLUE_DARK)

        # Text for instructions for new game/return to menu
        self.__font2 = pygame.font.SysFont("comicsansms", 20)
        self.__text_object_instru_when_won = self.__font2.render(
            "Press Enter to play again, or Escape to go to the menu", True, PURPLE)

        # Messages to invite a player to play
        if self.__player == 1:
            self.__text_object_invite_player = self.__font2.render(
                "Player 1, your turn, JUST DO IT !!!", True, RED)
        elif self.__player == 2:
            self.__text_object_invite_player = self.__font2.render(
                "Player 2, your turn, JUST DO IT !!!", True, BLUE)
        elif self.__player == 0:
            self.__text_object_invite_player1 = self.__font2.render(
                "Player 1, your turn, JUST DO IT !!!", True, RED)
            self.__text_object_invite_player2 = self.__font2.render(
                "Player 2, your turn, JUST DO IT !!!", True, BLUE)

    def reset_board(self):
        """Removes all tokens"""
        self.__board.reset()

    def set_token(self, token, i, j, k):
        """Sets a token in the (i, j, k) cube"""
        self.__board.set_token(i, j, k, token)

    def run(self):
        """Launches the GUI"""

        running = True
        clock = pygame.time.Clock()
        timer = pygame.time.get_ticks()

        # Keep in memory which arrow is pressed
        arrow_up = False
        arrow_down = False
        arrow_left = False
        arrow_right = False
        right_click = False
        last_mouse_pos = 0, 0
        new_mouse_pos = 0, 0

        selected_cube = None

        winning_player = 0
        winning_line = []

        invited_player = 0

        # Main Loop
        while running:

            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__commObject.gui_add_event(["QUT"])
                    return "QUT"
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.__commObject.gui_add_event(["QUT"])
                    return "MEN"
                elif event.type == KEYDOWN and event.key == K_RETURN and winning_player != 0:
                    self.__commObject.gui_add_event(["RST"])

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
                elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                    right_click = True
                    last_mouse_pos = event.pos
                    new_mouse_pos = event.pos
                elif event.type == MOUSEBUTTONUP and event.button == 3:
                    right_click = False

                elif event.type == MOUSEMOTION:
                    selected_cube = self.__board.point_on_a_cube(event.pos)
                    if right_click:
                        new_mouse_pos = event.pos

                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    if self.__player > 0:
                        self.__commObject.gui_add_event(["CLK", selected_cube])
                    else:
                        if invited_player == 1:
                            self.__commObject.gui_add_event(["CLK", selected_cube])
                        elif invited_player == 2:
                            self.__commObject2.gui_add_event(["CLK", selected_cube])

            # Checking the commands the Main thread could have sent
            for event in self.__commObject.get_and_empty_Main_events():
                if event[0] == "QUT":
                    resp = DeconnectionScreen(self.__window).launch()
                    return resp
                elif event[0] == "SET":
                    self.set_token(event[1], event[2], event[3], event[4])
                    if event[1] == 1:
                        self.__sound_object.player_1()
                    elif event[1] == 2:
                        self.__sound_object.player_2()
                elif event[0] == "RST":
                    self.reset_board()
                    winning_player = 0
                    winning_line = []
                    invited_player = 0
                    self.__sound_object.play()
                elif event[0] == "WIN":
                    winning_player = event[1]
                    winning_line = event[2]
                    self.__board.view.set_angles(2 * np.pi / 18, 2 * np.pi / 18)
                    invited_player = 0
                    if self.__player == 0:
                        self.__sound_object.victory()
                    elif winning_player == self.__player:
                        self.__sound_object.victory()
                    else:
                        self.__sound_object.defeat()
                elif event[0] == "INV":
                    invited_player = event[1]

            # If local 2 player, no need to listen to the 2nd commClient, we just empty it
            if self.__player == 0:
                self.__commObject2.get_and_empty_Main_events()

            # Now we take care of the grid rotation
            new_timer = pygame.time.get_ticks()
            elapsed = (new_timer - timer) / 1000
            timer = new_timer
            if winning_player == 0:
                if arrow_up:
                    self.__board.view.rotate(0, self.__rotation_speed * elapsed)
                if arrow_down:
                    self.__board.view.rotate(0, -self.__rotation_speed * elapsed)
                if arrow_left:
                    self.__board.view.rotate(1, -self.__rotation_speed * elapsed)
                if arrow_right:
                    self.__board.view.rotate(1, self.__rotation_speed * elapsed)
                if right_click:
                    x_delta = new_mouse_pos[0] - last_mouse_pos[0]
                    y_delta = new_mouse_pos[1] - last_mouse_pos[1]
                    self.__board.view.rotate(1, -self.__rotation_speed_mouse * x_delta)
                    self.__board.view.rotate(0, self.__rotation_speed_mouse * y_delta)
                    last_mouse_pos = new_mouse_pos
            else:
                self.__board.view.rotate(1, self.__rotation_when_won * elapsed)

            # Now we draw everything

            self.__window.screen.fill((0, 0, 0))
            self.__board.draw(self.__window.screen, selected_cube, winning_player, winning_line)
            window_dim = self.__window.get_dimension()
            if winning_player == 1:
                text_dim = self.__text_object_winner_1.get_size()
                self.__window.screen.blit(
                    self.__text_object_winner_1,
                    (((window_dim[0] - text_dim[0]) // 2),
                     ((window_dim[1] - text_dim[1]) // 8)))
            elif winning_player == 2:
                text_dim = self.__text_object_winner_2.get_size()
                self.__window.screen.blit(
                    self.__text_object_winner_2,
                    (((window_dim[0] - text_dim[0]) // 2),
                     ((window_dim[1] - text_dim[1]) // 8)))

            if winning_player != 0:
                text_dim = self.__text_object_instru_when_won.get_size()
                self.__window.screen.blit(
                    self.__text_object_instru_when_won,
                    (((window_dim[0] - text_dim[0]) // 2),
                     (48 * (window_dim[1] - text_dim[1]) // 50)))

            if self.__player > 0 and invited_player == self.__player:
                text_dim = self.__text_object_invite_player.get_size()
                self.__window.screen.blit(
                    self.__text_object_invite_player,
                    (((window_dim[0] - text_dim[0]) // 2),
                     (48 * (window_dim[1] - text_dim[1]) // 50)))
            elif self.__player == 0 and invited_player == 1:
                text_dim = self.__text_object_invite_player1.get_size()
                self.__window.screen.blit(
                    self.__text_object_invite_player1,
                    (((window_dim[0] - text_dim[0]) // 2),
                     (48 * (window_dim[1] - text_dim[1]) // 50)))
            elif self.__player == 0 and invited_player == 2:
                text_dim = self.__text_object_invite_player2.get_size()
                self.__window.screen.blit(
                    self.__text_object_invite_player2,
                    (((window_dim[0] - text_dim[0]) // 2),
                     (48 * (window_dim[1] - text_dim[1]) // 50)))


            pygame.display.flip()
            clock.tick(60)
