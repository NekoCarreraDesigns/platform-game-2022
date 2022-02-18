# imports for platform game
import pygame
import sys
from settings import *

# pygame global variables
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


# caption and title
pygame.display.set_caption("Pimp-ee-yo: The Game Is to Be Sold, Not Told")
captionImg = pygame.image.load('pimp.png')
pygame.display.set_icon(captionImg)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    pygame.display.update()
    clock.tick(120)
