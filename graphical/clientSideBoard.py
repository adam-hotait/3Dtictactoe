import pygame
from graphical.cube import Cube
from graphical.view import View
from graphical.colors import *


class ClientSideBoard():
    """Class that represents the board as it will be displayed"""
    
    def __init__(self):
        """Constructor. Default values of attributes (can be modified later)"""
        
        self.position = 50, 50
        
        self.size = 20, 20
        
        self.cube_color = GREY_SEMI
        
        self.cross_color = RED
        
        self.circle_color = BLUE
        
        self.cube_with_cross_color = RED_SEMI
        
        self.cube_with_circle_color = BLUE_SEMI
        
        self.cube_selected_color = GREEN_SEMI
        
        self.background_color = WHITE
        
        self.view = View()
        
        self.__size_cubes = min(self.size[0], self.size[1]) / 9
        
        self.space_between_cubes = 1 #Fraction of the cubes' size
        
        self.cubes = None #Will be initialized in the generate method
        
    
    def generate(self):
        """Generates cubes. Must be called after the board position and dimension have been set"""
        #Creation of the cubes in 3D space
        #Cubes are indexed in the list with the front-top-left cube being (0, 0, 0) (but these are not its coordinates in the 3d space)

        self.__size_cubes = min(self.size[0], self.size[1]) / 8
        space = self.__size_cubes *(1 +  self.space_between_cubes)
        self.__cubes = [
                    [[Cube((-space, -space, -space), self.__size_cubes, (0, 0, 0)), Cube((0, -space, -space), self.__size_cubes, (1, 0, 0)), Cube((space, -space, -space), self.__size_cubes, (2, 0, 0))],
                    [Cube((-space, 0, -space), self.__size_cubes, (0, 1, 0)), Cube((0, 0, -space), self.__size_cubes, (1, 1, 0)), Cube((space, 0, -space), self.__size_cubes, (2, 1, 0))],
                    [Cube((-space, space, -space), self.__size_cubes, (0, 2, 0)), Cube((0, space, -space), self.__size_cubes, (1, 2, 0)), Cube((space, space, -space), self.__size_cubes, (2, 2, 0))]],
                    [[Cube((-space, -space, 0), self.__size_cubes, (0, 0, 1)), Cube((0, -space, 0), self.__size_cubes, (1, 0, 1)), Cube((space, -space, 0), self.__size_cubes, (2, 0, 1))],
                    [Cube((-space, 0, 0), self.__size_cubes, (0, 1, 1)), Cube((0, 0, 0), self.__size_cubes, (1, 1, 1)), Cube((space, 0, 0), self.__size_cubes, (2, 1, 1))],
                    [Cube((-space, space, 0), self.__size_cubes, (0, 2, 1)), Cube((0, space, 0), self.__size_cubes, (1, 2, 1)), Cube((space, space, 0), self.__size_cubes, (2, 2, 1))]],
                    [[Cube((-space, -space, space), self.__size_cubes, (0, 0, 2)), Cube((0, -space, space), self.__size_cubes, (1, 0, 2)), Cube((space, -space, space), self.__size_cubes, (2, 0, 2))],
                    [Cube((-space, 0, space), self.__size_cubes, (0, 1, 2)), Cube((0, 0, space), self.__size_cubes, (1, 1, 2)), Cube((space, 0, space), self.__size_cubes, (2, 1, 2))],
                    [Cube((-space, space, space), self.__size_cubes, (0, 2, 2)), Cube((0, space, space), self.__size_cubes, (1, 2, 2)), Cube((space, space, space), self.__size_cubes, (2, 2, 2))]]]
        
        for cubess in self.__cubes:
            for cubes in cubess:
                for cube in cubes:
                    cube.apply_rotation(self.view.get_rotation())
        
        
    def get_token(self, i, j, k):
        """Returns the token in the cube (i, j, k), 0 if None"""
        return self.__cubes[i][j][k].get_token()
    
    def set_token(self, i, j, k, token):
        """Sets a token in the (i, j, k) cube"""
        self.__cubes[i][j][k].set_token(token)
    
    def reset(self):
        """Removes all tokens"""
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.set_token(i, j, k, 0)
    
    
    def draw(self, screen, selected=None):
        """Draws the board on the screen. Optional parameter "selected" indicates which cube must be highlighted"""
        
        #Background
        background = pygame.rect.Rect(self.position, self.size)
        pygame.draw.rect(screen, self.background_color, background)
        
        #We put all cubes in a list
        cubes = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    cubes.append(self.__cubes[i][j][k])
        
        #We apply the rotation
        for cube in cubes:
            cube.apply_rotation(self.view.get_rotation())
        
        #We sort the list so the deepest cube will be drawn first
        cubes.sort(reverse=True)
        
        for cube in cubes:
            token = cube.get_token()
            if token == 1:
                cube.draw(screen, self.cube_with_cross_color, self.position, self.size, self.cross_color)
            elif token == 2:
                cube.draw(screen, self.cube_with_circle_color, self.position, self.size, self.circle_color)
            else:
                if selected and cube.get_index() == selected:
                    cube.draw(screen, self.cube_selected_color, self.position, self.size)
                else:
                    cube.draw(screen, self.cube_color, self.position, self.size)
        
    def point_on_a_cube(self, pos):
        """We want to know if the cursor at pos is hovering a cube. Returns (i, j, k) if cursor is above this cube, None if it is not hovering a cube"""
        #Firstly we sort cubes by depth
        cubes = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    cubes.append(self.__cubes[i][j][k])
        cubes.sort()
        
        
        #Then we check each cube
        for cube in cubes:
            if cube.point_in_cube(pos, self.position, self.size):
                return cube.get_index()
        
        #Not on a cube
        return None
                    