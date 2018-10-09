import pygame
from pygame.locals import *
from clientSideBoard import ClientSideBoard


pygame.init()
w, h = 1280, 720
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Hello")

example_board = [
            [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 2]]]

            
board = ClientSideBoard()
size = min(w, h)
board.size = (size, size)
board.position = ((w - size) / 2, (h - size) / 2)

board.generate()
            
for i in range(3):
    for j in range(3):
        for k in range(3):
            
            board.set_token(i, j, k, example_board[i][j][k])

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            index = board.point_on_a_cube(event.pos)
            if index:
                print("Detected click on ", index)
    
    screen.fill((0, 0, 0))
    board.draw(screen, selected=(1, 1, 1))
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
    