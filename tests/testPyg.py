import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 500))
print(pygame.display.get_driver())

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((0, 0, 255))
    pygame.draw.rect(screen, (255, 0, 0), pygame.rect.Rect((10, 10), (100, 100)))

    pygame.display.flip()

pygame.quit()