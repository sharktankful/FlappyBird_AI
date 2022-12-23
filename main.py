import pygame
import neat
import random
import os
import sys

# INTITALIZE PYGAME
pygame.init()

# SCREEN VARIABLE DIMESNIONS
screen_width = 500
screen_height = 800

# IMAGES
bg_surface = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background-night.png')), (screen_width, screen_height))
floor = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'base.png')))


# CLASS DEFINES FLOOR ELEMENTS
class Floor:
    def __init__(self):
        self.floor = floor
        self.x = 0

    def move(self):
        self.x -= 2

    def draw(self, win):
        win.blit(self.floor, (self.x, 700))
        win.blit(self.floor, (self.x + 500, 700))

        if self.x <= -500:
            self.x = 0


# DRAWS OBJECTS/BACKGROUND IMAGES TO SCREEN
def draw_screen(win, floor):
    win.blit(bg_surface, (0, 0))
    floor.draw(win)
    pygame.display.update()


# MAIN GAME FUNCTION
def main():
    # FUNCTION VARIABLES
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((screen_width, screen_height))
    floor = Floor()

    # MAIN GAME LOOP
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit
                sys.exit()

        # MOVES FLOOR
        # floor.move()

        # PUTS IMAGES IN GAME
        draw_screen(win, floor)


main()
