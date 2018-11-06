import pygame
from pygame.locals import *
from client_side.graphical.menuOption import MenuOption
from client_side.graphical.inputAddress import InputAddress



class Menu:
    """Main menu of our game"""

    def __init__(self, window, sound_object):

        self.__window = window
        self.__fond = pygame.image.load("client_side/graphical/menu.jpg").convert()
        self.__fond = pygame.transform.scale(self.__fond, window.get_dimension())
        self.__sound_object = sound_object

        w, h = window.get_dimension()  # width and height of the window

        # Creation of the menu options

        #Local 2 players option
        local_option = MenuOption("Local 2 player", "LOCAL", (int((3 / 4) * w), int((1 / 20) * h)), (int((1 / 6) * w), int((1 / 20) * h)))

        # Join option
        join_option = MenuOption("Join Server", "JOIN", (int((3 / 4) * w), int((2.5 / 20) * h)), (int((1 / 6) * w), int((1 / 20) * h)))

        # Create option
        create_option = MenuOption("Create Server", "CREATE", (int((3 / 4) * w), int((4 / 20) * h)), (int((1 / 6) * w), int((1 / 20) * h)))

        # Music option
        music_option = MenuOption("Toggle music", "MUSIC", (int((3 / 4) * w), int((5.5 / 20) * h)),
                                   (int((1 / 6) * w), int((1 / 20) * h)))

        # Quit option
        quit_option = MenuOption("Quit", "QUIT", (int((3 / 4) * w), int((7 / 20) * h)), (int((1 / 6) * w), int((1 / 20) * h)))

        self.__options = [local_option, join_option, create_option, music_option, quit_option]

        self.__server_address = None

    @property
    def server_address(self):
        return self.__server_address

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

            selected_rect = -1  # index of the selected rectangle, -1 if no rectangle is selected

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
                            self.__sound_object.player_1()
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
                            self.__sound_object.player_1()

                # Display
                self.__window.screen.fill((0, 0, 0))
                self.__window.screen.blit(self.__fond, (0, 0))
                for k in range(len(self.__options)):
                    option = self.__options[k]

                    if k == selected_rect:
                        option.draw(self.__window.screen, True)
                    else:
                        option.draw(self.__window.screen, False)

                pygame.display.flip()
                clock.tick(60)

            # Now a button has been clicked on. If it is the "join server" button, we must ask the server address
            clicked_option = self.__options[clicked]
            if clicked_option.return_text == "JOIN":
                
                w, h = self.__window.get_dimension()

                position = (
                    int((1 / 3) * w),
                    int((1 / 20) * h))
                size = (
                    int((w - position[0]) / 2),
                    int((h - position[1]) / 2))
                inputBox = InputAddress(position, size)

                selected_rect = -1

                ip_entered = False
                go_back_to_menu = False

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
                                # A button has been clicked on
                                self.__sound_object.player_1()
                                return_text = inputBox.get_button_mesage_from_index(clicked)
                                if return_text == "RETURN":
                                    go_back_to_menu = True
                                elif return_text == "LH":
                                    self.__server_address = "127.0.0.1"
                                    ip_entered = True
                                elif return_text == "OK":
                                    self.__server_address = inputBox.get_input_text()
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
                                self.__sound_object.player_1()
                                # A button has been selected and entered
                                return_text = inputBox.get_button_mesage_from_index(selected_rect)
                                if return_text == "RETURN":
                                    go_back_to_menu = True
                                elif return_text == "LH":
                                    self.__server_address = "127.0.0.1"
                                    ip_entered = True
                                elif return_text == "OK":
                                    print("OK")
                                    self.__server_address = inputBox.get_input_text()
                                    ip_entered = True

                            else:
                                self.__server_address = inputBox.get_input_text()
                                ip_entered = True

                        elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                            inputBox.removeChar()
                        elif event.type == KEYDOWN:
                            inputBox.addChar(event.unicode)

                    # Display

                    self.__window.screen.fill((0, 0, 0))
                    self.__window.screen.blit(self.__fond, (0, 0))
                    for k in range(len(self.__options)):
                        option = self.__options[k]
                        option.draw(self.__window.screen, False)
                    inputBox.draw(self.__window.screen, selected_rect)
                    pygame.display.flip()
                    clock2.tick(60)
                # If an IP has been entered, we can stop this function here, else we do it again
                if ip_entered:
                    return "JOIN"

            # If the clicked button was not "join":
            elif clicked_option.return_text == "MUSIC":
                self.__sound_object.toggle()
            else:
                return clicked_option.return_text
