import pygame


class Sound:
    """Class that manages all sounds (music and sound effects)"""

    def __init__(self):
        """Constructor"""

        try:
            pygame.mixer.music.load("client_side/sound/Tetris.mp3")
            pygame.mixer.music.set_volume(0.5)

            self.__victory_music = pygame.mixer.Sound("client_side/sound/victory.wav")
            self.__defeat_music = pygame.mixer.Sound("client_side/sound/defeat.wav")
            self.__selection_player_1 = pygame.mixer.Sound("client_side/sound/selection_player_1.wav")
            self.__selection_player_2 = pygame.mixer.Sound("client_side/sound/selection_player_2.wav")
            self.__is_muted = False
            self.__not_initialized = False
        except FileNotFoundError as e:
            print("Error with sound files, continuing anyway")
            print(e)
            self.__is_muted = True
            self.__not_initialized = True

    def play(self):
        """Plays music"""
        pygame.mixer.stop()
        if not self.__is_muted:
            pygame.mixer.music.play(-1)

    def victory(self):
        """Plays ictory music"""
        pygame.mixer.music.stop()
        if not self.__is_muted:
            self.__victory_music.play()

    def defeat(self):
        """Plays defeat music"""
        pygame.mixer.music.stop()
        if not self.__is_muted:
            self.__defeat_music.play()

    def player_1(self):
        """Plays player 1 click sound"""
        if not self.__is_muted:
            self.__selection_player_1.play()

    def player_2(self):
        """Plays player 2 click sound"""
        if not self.__is_muted:
            self.__selection_player_1.play()

    def stop(self):
        """Stops music"""
        pygame.mixer.music.stop()

    def mute(self):
        """Mutes sounds and music"""
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.__is_muted = True

    def unmute(self):
        """Unmutes sounds and music"""
        if not self.__not_initialized:
            self.__is_muted = False
            pygame.mixer.music.play(-1)

    def toggle(self):
        """Toggles if music is muted or not"""
        if self.__is_muted:
            self.unmute()
        else:
            self.mute()
