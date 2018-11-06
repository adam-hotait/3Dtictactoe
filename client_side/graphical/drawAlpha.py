# Just a few functions to draw shapes with alpha transparency (which the pygame draw function does not do)
import pygame


class DrawAlpha:
    """Wrapper class for draw-with-alpha functions"""
    
    @staticmethod
    def rect(screen, color, position, size):
        """Draws a rectangle with transparency"""
        if len(color) < 4:
            pygame.draw.rect(screen, position, pygame.rect.Rect(position, size))
        else:
            surface = pygame.Surface((size))
            surface.set_alpha(color[3])
            surface.fill((color[0], color[1], color[2]))
            screen.blit(surface, position)
    
    @staticmethod
    def polygon(screen, color, points):
        """Draws a polygon with transparency"""
        if len(color) < 4:
            pygame.draw.polygon(screen, color, points)
        else:
            # We must create a rectangular surface to contain the polygon
            min_x = float('inf')
            min_y = float('inf')
            max_x = -float('inf')
            max_y = -float('inf')
            for point in points:
                if point[0] < min_x:
                    min_x = point[0]
                if point[1] < min_y:
                    min_y = point[1]
                if point[0] > max_x:
                    max_x = point[0]
                if point[1] > max_y:
                    max_y = point[1]
             
            # Transformation in integers:
            min_x, min_y, max_x, max_y = map(int, [min_x, min_y, max_x, max_y])
            
            surface = pygame.Surface((max_x - min_x, max_y - min_y))
            surface.set_colorkey((0, 0, 0))
            surface.set_alpha(color[3])
            # Translation of the points to be in the surface:
            new_points = []
            for point in points:
                new_points.append((point[0] - min_x, point[1] - min_y))
            
            pygame.draw.polygon(surface, color, new_points)
            screen.blit(surface, (min_x, min_y))
