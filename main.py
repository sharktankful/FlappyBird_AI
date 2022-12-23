import pygame
import neat
import random
import os
import sys

# INTITALIZE PYGAME
pygame.init()

screen_width = 500
screen_height = 800

# IMAGES
bg_surface = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background-night.png')), (screen_width, screen_height))


# DRAWS OBJECTS/BACKGROUND IMAGES TO SCREEN
def draw_screen(win):
    win.blit(bg_surface, (0, 0))
    pygame.display.update()


# MAIN GAME FUNCTION
def main():
    # FUNCTION VARIABLES
    win = pygame.display.set_mode((screen_width, screen_height))

    # MAIN GAME LOOP
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit
                sys.exit()

        draw_screen(win)


main()
