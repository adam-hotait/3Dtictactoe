import numpy as np
from graphical.colors import *
import pygame
from graphical.drawAlpha import DrawAlpha



class Cube():
    
    def __init__(self, center_pos, size, index):
    
        self.__token = 0 #0 if nothing, 1 for a cross and 2 for a circle
        
        self.__index = index
        
        self.__center = np.matrix([
                            [center_pos[0]],
                            [center_pos[1]],
                            [center_pos[2]]])
        
        self.__size = size
        
        #Position of points in 3D space if the cube was centered in 0,0,0 and size 2
        
        points = [
                        np.matrix([[-1], [-1], [-1]]),
                        np.matrix([[1], [-1], [-1]]),
                        np.matrix([[1], [1], [-1]]),
                        np.matrix([[-1], [1], [-1]]),
                        np.matrix([[-1], [-1], [1]]),
                        np.matrix([[1], [-1], [1]]),
                        np.matrix([[1], [1], [1]]),
                        np.matrix([[-1], [1], [1]])]
        
        #Translation of points to fit center and size:
        self.__points = []
        for point in points:
            self.__points.append(self.__center + (1/2) * point * self.__size)
        
        self.__rotated_points = None # Will be computed when we apply a rotation on the cube
        self.__rotated_center = None
    
    def get_token(self):
        return self.__token
    
    def set_token(self, new_token):
        self.__token = new_token
        
    def get_index(self):
        return self.__index
    
    def apply_rotation(self, rotation_matrix):
    
        self.__rotated_points = [
                    np.dot(rotation_matrix, point)
                    for point in self.__points ]
        
        self.__rotated_center = np.dot(rotation_matrix, self.__center)
    
    def get_depth(self):
        """Returns the depth of the cube in the point of vue given by the rotation matrix"""
        return self.__rotated_center[2][0]
    
    def __lt__(self, other):
        """Will let us order cubes by depth"""
        return self.get_depth() < other.get_depth()
    
    def draw(self, screen, color, pos, size, token_color=WHITE): #Position and size of the board in the window
    
        
        projeted_points = []
        for point in self.__rotated_points:
            projeted_points.append((
                        int(point[0][0] + pos[0] + (1/2) * size[0]),
                        int(point[1][0] + pos[1] + (1/2) * size[1])))
        projected_center = (
                    int(self.__rotated_center[0][0] + pos[0] + (1/2) * size[0]),
                    int(self.__rotated_center[1][0] + pos[1] + (1/2) * size[1]))
        
        #Let's create all 6 faces
        faces = []
        faces.append((projeted_points[0], projeted_points[1], projeted_points[2],projeted_points[3]))
        faces.append((projeted_points[0], projeted_points[1], projeted_points[5],projeted_points[4]))
        faces.append((projeted_points[1], projeted_points[2], projeted_points[6],projeted_points[5]))
        faces.append((projeted_points[0], projeted_points[4], projeted_points[7],projeted_points[3]))
        faces.append((projeted_points[2], projeted_points[6], projeted_points[7],projeted_points[3]))
        faces.append((projeted_points[4], projeted_points[5], projeted_points[6],projeted_points[7]))
        
        #Let's print them !
        for face in faces:
            DrawAlpha.polygon(screen, color, face)
        
        #Now we can print a cross or a circle
        #Cross:
        if self.__token == 1:
            cross_half_length = int(0.4 * self.__size)
            cross_width = int(0.1 * self.__size) + 1
            
            
            point_1 = (int(projected_center[0] + cross_half_length), int(projected_center[1] + cross_half_length))
            point_2 = (int(projected_center[0] - cross_half_length), int(projected_center[1] - cross_half_length))
            point_3 = (int(projected_center[0] + cross_half_length), int(projected_center[1] - cross_half_length))
            point_4 = (int(projected_center[0] - cross_half_length), int(projected_center[1] + cross_half_length))
            
            
            pygame.draw.line(screen, token_color, point_1, point_2, cross_width)
            pygame.draw.line(screen, token_color, point_3, point_4, cross_width)
        #Circle
        elif self.__token == 2:
            circle_radius = int(self.__size * 0.4)
            pygame.draw.circle(screen, token_color, projected_center, circle_radius)
            
    def point_in_cube(self, pos, board_pos, board_size): #size of the board in the window
        
        projected_center = (
                    self.__rotated_center[0][0] + board_pos[0] + (1/2) * board_size[0],
                    self.__rotated_center[1][0] + board_pos[1] + (1/2) * board_size[1])
                    
        min_x = int(projected_center[0] - self.__size / 2)
        min_y = int(projected_center[1] - self.__size / 2)
        max_x = int(projected_center[0] + self.__size / 2)
        max_y = int(projected_center[1] + self.__size / 2)
        
        if pos[0] >= min_x and pos[0] <= max_x and pos[1] >= min_y and pos[1] <= max_y :
            return True
        else:
            return False
        
        
        
        