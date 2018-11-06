import pygame

class Sound:
    """Class that manages all sounds (music and sound effects)"""

    def __init__(self):
        """Constructor"""

        pygame.mixer.music.load("sound/Tetris.mp3")
        pygame.mixer.music.set_volume(0.5)
        self.__victory_music = pygame.mixer.Sound("sound/victory.wav")
        self.__defeat_music = pygame.mixer.Sound("sound/defeat.wav")
        self.__selection_player_1 = pygame.mixer.Sound("sound/selection_player_1.wav")
        self.__selection_player_2 = pygame.mixer.Sound("sound/selection_player_2.wav")

        self.__is_muted = False



    def play(self):
        pygame.mixer.stop()
        if not self.__is_muted:
            pygame.mixer.music.play(-1)

    def victory(self):
        pygame.mixer.music.stop()
        if not self.__is_muted:
            self.__victory_music.play()

    def defeat(self):
        pygame.mixer.music.stop()
        if not self.__is_muted:
            self.__defeat_music.play()

    def player_1(self):
        if not self.__is_muted:
            self.__selection_player_1.play()

    def player_2(self):
        if not self.__is_muted:
            self.__selection_player_1.play()

    def stop(self):
        pygame.mixer.music.stop()

    def mute(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.__is_muted = True

    def unmute(self):
        self.__is_muted = False
        pygame.mixer.music.play(-1)

    def toggle(self):
        if self.__is_muted:
            self.unmute()
        else:
            self.mute()