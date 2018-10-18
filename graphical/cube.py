import numpy as np
from .colors import *
import pygame
from .drawAlpha import DrawAlpha



class Cube():
    """A class that represents a cube as it will be displayed on screen"""
    def __init__(self, center_pos, size, index):
        """Constructor, creates the cube and calculates its coordinates in the default view"""
    
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
        """Returns the token of the cube"""
        return self.__token
    
    def set_token(self, new_token):
        """Sets the token of the cube"""
        self.__token = new_token
        
    def get_index(self):
        """Returns the index (i, j, k) of the cube in the board"""
        return self.__index
    
    def apply_rotation(self, rotation_matrix):
        """Rotates the cube by the given rotation matrix"""
    
        self.__rotated_points = [
                    np.dot(rotation_matrix, point)
                    for point in self.__points]
        
        self.__rotated_center = np.dot(rotation_matrix, self.__center)
    
    def get_depth(self):
        """Returns the depth of the cube in the point of vue given by the rotation matrix"""
        return self.__rotated_center[2][0]
    
    def __lt__(self, other):
        """Will let us order cubes by depth"""
        return self.get_depth() < other.get_depth()
    
    def draw(self, screen, color, pos, size, token_color=WHITE): #Position and size of the board in the window
        """Draws the cube on the screen, with the given color (handles alpha)"""
        
        projeted_points = []
        for point in self.__rotated_points:
            projeted_points.append((
                        int(point[0][0] + pos[0] + (1/2) * size[0]),
                        int(point[1][0] + pos[1] + (1/2) * size[1])))
        projected_center = (
                    int(self.__rotated_center[0][0] + pos[0] + (1/2) * size[0]),
                    int(self.__rotated_center[1][0] + pos[1] + (1/2) * size[1]))

        #Let's find the closest point
        closest_point_index = 0
        for k in range(len(self.__rotated_points)):
            if self.__rotated_points[k][2] < self.__rotated_points[closest_point_index][2]:
                closest_point_index = k

        #Let's find the 3 faces that this point touches
        faces = []
        if closest_point_index in (0,1,2,3):
            faces.append((projeted_points[0], projeted_points[1], projeted_points[2], projeted_points[3]))
        else:
            faces.append((projeted_points[4], projeted_points[5], projeted_points[6], projeted_points[7]))
        if closest_point_index in (0,1,5,4):
            faces.append((projeted_points[0], projeted_points[1], projeted_points[5], projeted_points[4]))
        else:
            faces.append((projeted_points[2], projeted_points[6], projeted_points[7], projeted_points[3]))
        if closest_point_index in (1,2,6,5):
            faces.append((projeted_points[1], projeted_points[2], projeted_points[6], projeted_points[5]))
        else:
            faces.append((projeted_points[0], projeted_points[4], projeted_points[7], projeted_points[3]))


        
        #Let's print them !
        for face in faces:
            DrawAlpha.polygon(screen, color, face)

        #Let's find the 9 edges that can be visible:
        if closest_point_index == 0:
            edges = [
                (projeted_points[0], projeted_points[1]),
                (projeted_points[0], projeted_points[3]),
                (projeted_points[0], projeted_points[4]),
                (projeted_points[2], projeted_points[3]),
                (projeted_points[4], projeted_points[7]),
                (projeted_points[3], projeted_points[7]),
                (projeted_points[4], projeted_points[5]),
                (projeted_points[1], projeted_points[5]),
                (projeted_points[1], projeted_points[2])
            ]
        elif closest_point_index == 1:
            edges = [
                (projeted_points[0], projeted_points[1]),
                (projeted_points[0], projeted_points[3]),
                (projeted_points[0], projeted_points[4]),
                (projeted_points[2], projeted_points[3]),
                (projeted_points[4], projeted_points[5]),
                (projeted_points[1], projeted_points[5]),
                (projeted_points[1], projeted_points[2]),
                (projeted_points[6], projeted_points[5]),
                (projeted_points[6], projeted_points[2])
            ]
        elif closest_point_index == 2:
            edges = [
                (projeted_points[0], projeted_points[1]),
                (projeted_points[0], projeted_points[3]),
                (projeted_points[2], projeted_points[3]),
                (projeted_points[3], projeted_points[7]),
                (projeted_points[1], projeted_points[5]),
                (projeted_points[1], projeted_points[2]),
                (projeted_points[6], projeted_points[7]),
                (projeted_points[6], projeted_points[5]),
                (projeted_points[6], projeted_points[2])
            ]
        elif closest_point_index == 3:
            edges = [
                (projeted_points[0], projeted_points[1]),
                (projeted_points[0], projeted_points[3]),
                (projeted_points[0], projeted_points[4]),
                (projeted_points[2], projeted_points[3]),
                (projeted_points[4], projeted_points[7]),
                (projeted_points[3], projeted_points[7]),
                (projeted_points[1], projeted_points[2]),
                (projeted_points[6], projeted_points[7]),
                (projeted_points[6], projeted_points[2])
            ]
        elif closest_point_index == 4:
            edges = [
                (projeted_points[0], projeted_points[1]),
                (projeted_points[0], projeted_points[3]),
                (projeted_points[0], projeted_points[4]),
                (projeted_points[4], projeted_points[7]),
                (projeted_points[3], projeted_points[7]),
                (projeted_points[4], projeted_points[5]),
                (projeted_points[1], projeted_points[5]),
                (projeted_points[6], projeted_points[7]),
                (projeted_points[6], projeted_points[5]),
            ]
        elif closest_point_index == 5:
            edges = [
                (projeted_points[0], projeted_points[1]),
                (projeted_points[0], projeted_points[4]),
                (projeted_points[4], projeted_points[7]),
                (projeted_points[4], projeted_points[5]),
                (projeted_points[1], projeted_points[5]),
                (projeted_points[1], projeted_points[2]),
                (projeted_points[6], projeted_points[7]),
                (projeted_points[6], projeted_points[5]),
                (projeted_points[6], projeted_points[2])
            ]
        elif closest_point_index == 6:
            edges = [
                (projeted_points[2], projeted_points[3]),
                (projeted_points[4], projeted_points[7]),
                (projeted_points[3], projeted_points[7]),
                (projeted_points[4], projeted_points[5]),
                (projeted_points[1], projeted_points[5]),
                (projeted_points[1], projeted_points[2]),
                (projeted_points[6], projeted_points[7]),
                (projeted_points[6], projeted_points[5]),
                (projeted_points[6], projeted_points[2])
            ]
        elif closest_point_index == 7:
            edges = [
                (projeted_points[0], projeted_points[3]),
                (projeted_points[0], projeted_points[4]),
                (projeted_points[2], projeted_points[3]),
                (projeted_points[4], projeted_points[7]),
                (projeted_points[3], projeted_points[7]),
                (projeted_points[4], projeted_points[5]),
                (projeted_points[6], projeted_points[7]),
                (projeted_points[6], projeted_points[5]),
                (projeted_points[6], projeted_points[2])
            ]
        #Now we draw them
        for edge in edges:
            pygame.draw.line(screen, BLACK, edge[0], edge[1], 2)
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
        """Tells if the cursor is on the cube"""
        
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
        
        
        
        