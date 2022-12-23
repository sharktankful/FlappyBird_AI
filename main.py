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
floor_surface = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'base.png')))
pipes_surface = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'pipe-green.png')))

# TIMED EVENTS
pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, 2800)


# CLASS DEFINES FLOOR ELEMENTS
class Floor:
    def __init__(self):
        self.floor_surface = floor_surface
        self.x = 0

    def move(self):
        self.x -= 2

    def draw(self, win):
        win.blit(self.floor_surface, (self.x, 700))
        win.blit(self.floor_surface, (self.x + 500, 700))

        if self.x <= -500:
            self.x = 0


# CLASS DEFINES FLOOR ELEMENTS
class Pipes:
    def __init__(self):
        self.pipe_list = []

        self.pipes_surface_bottom = pipes_surface
        self.pipes_surface_top = pygame.transform.flip(
            pipes_surface, False, True)

    def create_pipe_rect(self):
        height = random.randrange(270, 610)

        pipes_surface_bottom_rect = self.pipes_surface_bottom.get_rect(
            midtop=(580, height))
        pipes_surface_top_rect = self.pipes_surface_top.get_rect(
            midbottom=(580, height - 200))

        return pipes_surface_bottom_rect, pipes_surface_top_rect

    def move(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 2

    def draw(self, win):
        for pipe in self.pipe_list:
            if pipe.bottom >= 800:
                win.blit(self.pipes_surface_bottom, pipe)
            else:
                win.blit(self.pipes_surface_top, pipe)


# DRAWS OBJECTS/BACKGROUND IMAGES TO SCREEN
def draw_screen(win, floor, pipes):
    win.blit(bg_surface, (0, 0))
    pipes.draw(win)
    floor.draw(win)
    pygame.display.update()


# MAIN GAME FUNCTION
def main():
    # FUNCTION VARIABLES
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((screen_width, screen_height))
    floor = Floor()
    pipes = Pipes()

    # MAIN GAME LOOP
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit
                sys.exit()
            if event.type == pipe_spawn:
                pipes.pipe_list.extend(pipes.create_pipe_rect())

        for pipe in pipes.pipe_list:
            if pipe.centerx < -50:
                pipes.pipe_list.remove(pipe)

        # MOVES FLOOR
        floor.move()

        # MOVES PIPE
        pipes.move()

        # PUTS IMAGES IN GAME
        draw_screen(win, floor, pipes)


main()