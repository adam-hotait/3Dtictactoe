import numpy as np

class View():
    
    initial_horizontal_angle = 2 * np.pi / 12
    initial_vertical_angle = 2 * np.pi / 12
    
    def __init__(self):
        
        self.__rotation = np.dot(self.__create_rotation_matrix(1, View.initial_horizontal_angle), self.__create_rotation_matrix(0, View.initial_vertical_angle))
    
    def __create_rotation_matrix(self, axis, angle):
        if axis == 0: #Rotation of axis x:
            return np.matrix((
                    (1, 0, 0),
                    (0, np.cos(angle), -np.sin(angle)),
                    (0, np.sin(angle), np.cos(angle))))
        elif axis == 1: #Rotation of axis y:
            return np.matrix((
                    (np.cos(angle), 0, np.sin(angle)),
                    (0, 1, 0),
                    (-np.sin(angle), 0, np.cos(angle))))
        elif axis == 2: #Rotation of axis z:
            return np.matrix((
                    (np.cos(angle), -np.sin(angle), 0),
                    (np.sin(angle), np.cos(angle), 0)
                    (0, 0, 1)))
    
    def rotate(self, axis, angle):
        self.__rotation = np.dot(self.__create_rotation_matrix(axis, angle), self.__rotation)
    
    def get_rotation(self):
        return self.__rotation
    
    def set_angles(self, horizontal, vertical):
        self.__rotation = np.dot(self.__create_rotation_matrix(1, vertical), self.__create_rotation_matrix(1, horizontal))
    
        