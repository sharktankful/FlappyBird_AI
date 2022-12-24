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

# GAME FONT/COLOR
game_font = pygame.font.SysFont('comicsans', 50)
white = (255, 255, 255)

# IMAGES
bg_surface = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background-night.png')), (screen_width, screen_height))
floor_surface = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'base.png')))
pipes_surface = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'pipe-green.png')))
upflap_surface = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'yellowbird-upflap.png')))
midflap_surface = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'yellowbird-midflap.png')))
downflap_surface = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'yellowbird-downflap.png')))
bird_surfaces = [upflap_surface, midflap_surface, downflap_surface]

# TIMED EVENTS
pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, 1900)
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 0.40
        self.movement = 0
        self.flap_number = 0
        self.bird_surface = bird_surfaces
        self.bird_surface_rect = self.bird_surface[self.flap_number].get_rect(center=(self.x, self.y))
    
    def move(self):
        self.movement += self.gravity
        self.bird_surface_rect.centery += self.movement
    
    def jump (self):
        self.movement = 0
        self.movement -= 6
    
    def collide(self, pipes):
        for pipe in pipes.pipe_list:
            if self.bird_surface_rect.colliderect(pipe):
                return True

    def bird_animation(self):
        if self.flap_number < 2:
            self.flap_number += 1
        else:
            self.flap_number = 0

    def draw(self, win):
        rotate_bird = pygame.transform.rotozoom(self.bird_surface[self.flap_number], -self.movement * 3, 1)
        win.blit(rotate_bird, self.bird_surface_rect)

# CLASS DEFINES FLOOR ELEMENTS
class Floor:
    def __init__(self):
        self.floor_surface = floor_surface
        self.x = 0

    def move(self):
        self.x -= 3

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
            pipe.centerx -= 3

    def draw(self, win):
        for pipe in self.pipe_list:
            if pipe.bottom >= 800:
                win.blit(self.pipes_surface_bottom, pipe)
            else:
                win.blit(self.pipes_surface_top, pipe)

# UPDATES CURERNT SCORE IN GAME
def update_score(pipes):
    for pipe in pipes.pipe_list:
        if pipe.centerx == 100:
            return True


# DRAWS OBJECTS/BACKGROUND IMAGES TO SCREEN
def draw_screen(win, floor, pipes, bird, score):
    win.blit(bg_surface, (0, 0))
    pipes.draw(win)
    floor.draw(win)
    bird.draw(win)

    score_label = game_font.render(f'Score: {score}', 1, white)
    win.blit(score_label, (300, 200))
    
    pygame.display.update()


# MAIN GAME FUNCTION
def main():
    # FUNCTION VARIABLES
    score = 0
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((screen_width, screen_height))
    floor = Floor()
    pipes = Pipes()
    bird = Bird(100, 200)

    # MAIN GAME LOOP
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
            if event.type == pipe_spawn:
                pipes.pipe_list.extend(pipes.create_pipe_rect())
            if event.type == bird_flap:
                bird.bird_animation()

        # PIPES WILL MOVE ACROSS THE SCREEN (FROM RIGHT TO LEFT)
        for pipe in pipes.pipe_list:
            if pipe.centerx < -50:
                pipes.pipe_list.remove(pipe)
        
        # IF BIRD COLLIDES WITH PIPE OR FLOOR/CEILING, THE GAME WILL END
        if bird.collide(pipes) == True:
            run = False
            print('GAME OVER!')
        elif bird.bird_surface_rect.centery >= 620 or bird.bird_surface_rect.centery <= -10:  
            run = False
            print('GAME OVER!')

        if update_score(pipes) == True:
            score += 1
        

        # MOVES FLOOR
        floor.move()

        # MOVES PIPE
        pipes.move()

        # APPLIES GRAVITY TO BIRD
        bird.move()

        # PUTS IMAGES IN GAME
        draw_screen(win, floor, pipes, bird, score)


main()
