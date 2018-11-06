import pygame
from .cube import Cube
from .view import View
from .colors import *


class ClientSideBoard:
    """Class that represents the board as it will be displayed"""

    def __init__(self):
        """Constructor. Default values of attributes (can be modified later)"""
        self.__position = 50, 50
        self.__size = 20, 20
        self.__cube_color = GREY
        self.__cross_color = RED
        self.__circle_color = BLUE
        self.__cube_with_cross_color = RED_SEMI
        self.__cube_with_circle_color = BLUE_SEMI
        self.__cube_selected_color = GREEN
        self.__background_color = WHITE
        self.__view = View()
        self.__size_cubes = min(self.__size[0], self.__size[1]) / 9
        self.__space_between_cubes = 1  # Fraction of the cubes' size
        self.__cubes = None  # Will be initialized in the generate method
        self.__background = None
        self.__background = pygame.image.load("graphical/background_board.png")

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

    @property
    def view(self):
        return self.__view

    def generate(self):
        """Generates cubes. Must be called after the board position and dimension have been set"""
        # Creation of the cubes and axis in 3D space
        # Cubes are indexed in the list with the front-top-left cube being (0, 0, 0)
        # (but these are not its coordinates in the 3D space)

        self.__size_cubes = min(self.__size[0], self.__size[1]) / 8
        space = self.__size_cubes * (1 + self.__space_between_cubes)
        self.__cubes = [
            [[Cube((-space, -space, -space), self.__size_cubes, (0, 0, 0)),
              Cube((0, -space, -space), self.__size_cubes, (1, 0, 0)),
              Cube((space, -space, -space), self.__size_cubes, (2, 0, 0))],
             [Cube((-space, 0, -space), self.__size_cubes, (0, 1, 0)),
              Cube((0, 0, -space), self.__size_cubes, (1, 1, 0)),
              Cube((space, 0, -space), self.__size_cubes, (2, 1, 0))],
             [Cube((-space, space, -space), self.__size_cubes, (0, 2, 0)),
              Cube((0, space, -space), self.__size_cubes, (1, 2, 0)),
              Cube((space, space, -space), self.__size_cubes, (2, 2, 0))]],
            [[Cube((-space, -space, 0), self.__size_cubes, (0, 0, 1)),
              Cube((0, -space, 0), self.__size_cubes, (1, 0, 1)),
              Cube((space, -space, 0), self.__size_cubes, (2, 0, 1))],
             [Cube((-space, 0, 0), self.__size_cubes, (0, 1, 1)), Cube((0, 0, 0), self.__size_cubes, (1, 1, 1)),
              Cube((space, 0, 0), self.__size_cubes, (2, 1, 1))],
             [Cube((-space, space, 0), self.__size_cubes, (0, 2, 1)), Cube((0, space, 0), self.__size_cubes, (1, 2, 1)),
              Cube((space, space, 0), self.__size_cubes, (2, 2, 1))]],
            [[Cube((-space, -space, space), self.__size_cubes, (0, 0, 2)),
              Cube((0, -space, space), self.__size_cubes, (1, 0, 2)),
              Cube((space, -space, space), self.__size_cubes, (2, 0, 2))],
             [Cube((-space, 0, space), self.__size_cubes, (0, 1, 2)), Cube((0, 0, space), self.__size_cubes, (1, 1, 2)),
              Cube((space, 0, space), self.__size_cubes, (2, 1, 2))],
             [Cube((-space, space, space), self.__size_cubes, (0, 2, 2)),
              Cube((0, space, space), self.__size_cubes, (1, 2, 2)),
              Cube((space, space, space), self.__size_cubes, (2, 2, 2))]]]

        for cubess in self.__cubes:
            for cubes in cubess:
                for cube in cubes:
                    cube.apply_rotation(self.__view.get_rotation())

    def get_token(self, i, j, k):
        """Returns the token in the cube (i, j, k), 0 if None"""
        return self.__cubes[k][j][i].get_token()

    def set_token(self, i, j, k, token):
        """Sets a token in the (i, j, k) cube"""
        print("set_token = ({},{},{}), with {}".format(i, j, k, token))
        self.__cubes[k][j][i].token = token

    def reset(self):
        """Removes all tokens"""
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.set_token(i, j, k, 0)
        self.__view = View()

    def draw(self, screen, selected=None, winning_player=0, winning_line=None):
        """Draws the board on the screen. Optional parameter "selected" indicates which cube must be highlighted"""

        # Allows for non-mutable optional argument
        if winning_line is None:
            winning_line = []

        # Background
        scaled_background = pygame.transform.scale(self.__background, pygame.display.get_surface().get_size())
        screen.blit(scaled_background, (self.__position, self.__size))

        # We put all cubes in a list
        cubes = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    cubes.append(self.__cubes[k][j][i])

        # We apply the rotation
        for cube in cubes:
            cube.apply_rotation(self.__view.get_rotation())

        # We sort the list so the deepest cube will be drawn first
        cubes.sort(reverse=True)

        for cube in cubes:
            if winning_player == 0:
                token = cube.token
                if token == 1:
                    cube.draw(screen, self.__cube_with_cross_color, self.__position, self.__size, self.__cross_color)
                elif token == 2:
                    cube.draw(screen, self.__cube_with_circle_color, self.__position, self.__size, self.__circle_color)
                else:
                    if selected and cube.index == selected:
                        cube.draw(screen, self.__cube_selected_color, self.__position, self.__size)
                    else:
                        cube.draw(screen, self.__cube_color, self.__position, self.__size)
            elif winning_player == 1:
                if cube.index in winning_line:
                    cube.token = 1
                    cube.draw(screen, self.__cube_with_cross_color, self.__position, self.__size, self.__cross_color)
                else:
                    cube.draw(screen, self.__cube_color, self.__position, self.__size)

            elif winning_player == 2:
                if cube.index in winning_line:
                    cube.token = 2
                    cube.draw(screen, self.__cube_with_circle_color, self.__position, self.__size, self.__circle_color)
                else:
                    cube.draw(screen, self.__cube_color, self.__position, self.__size)

    def point_on_a_cube(self, pos):
        """We want to know if the cursor at pos is hovering a cube. Returns (i, j, k) if cursor is above this cube,
        None if it is not hovering a cube"""
        # Firstly we sort cubes by depth
        cubes = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    cubes.append(self.__cubes[k][j][i])
        cubes.sort()

        # Then we check each cube
        for cube in cubes:
            if cube.point_in_cube(pos, self.__position, self.__size):
                return cube.index

        # Not on a cube
        return None
