import pygame
import neat 
import random
import os
import sys

# INTITALIZE PYGAME
pygame.init()

# WINDOW CAPTION
pygame.display.set_caption('AI Flappy Bird')

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

# CLASS DEFINES FLOOR BIRD
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 0.40
        self.movement = 0
        self.flap_number = 0
        self.bird_surface = bird_surfaces
        self.bird_surface_rect = self.bird_surface[self.flap_number].get_rect(
            center=(self.x, self.y))

    def move(self):
        self.movement += self.gravity
        self.bird_surface_rect.centery += self.movement

    def jump(self):
        self.movement = 0
        self.movement -= 7

    def bird_animation(self):
        if self.flap_number < 2:
            self.flap_number += 1
        else:
            self.flap_number = 0

    def draw(self, win):
        rotate_bird = pygame.transform.rotozoom(
            self.bird_surface[self.flap_number], -self.movement * 3, 1)
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
        # self.pipe_list = []
        self.pipe_passed = False
        self.height = random.randrange(300,600)
        self.pipes_surface_bottom = pipes_surface
        self.pipes_surface_bottom_rect = self.pipes_surface_bottom.get_rect(midtop=(550, self.height))
        self.pipes_surface_top = pygame.transform.flip(pipes_surface, False, True)
        self.pipes_surface_top_rect = self.pipes_surface_top.get_rect(midbottom=(550, self.height - 200))

    def move(self):
        self.pipes_surface_bottom_rect.centerx -= 3
        self.pipes_surface_top_rect.centerx -= 3

    def draw(self, win):
        win.blit(self.pipes_surface_top, self.pipes_surface_top_rect)
        win.blit(self.pipes_surface_bottom, self.pipes_surface_bottom_rect)


# DRAWS OBJECTS/BACKGROUND IMAGES TO SCREEN
def draw_screen(win, floor, pipes, bird, score):
    win.blit(bg_surface, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    floor.draw(win)
    bird.draw(win)

    score_label = game_font.render(f'Score: {score}', 1, white)
    win.blit(score_label, (screen_width - score_label.get_width() - 15, 10))

    pygame.display.update()


# MAIN GAME FUNCTION
def main():
    # FUNCTION VARIABLES
    score = 0
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((screen_width, screen_height))
    floor = Floor()
    pipes = [Pipes()]
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
            if event.type == bird_flap:
                bird.bird_animation()    


        # HOW PIPES WILL BEHAVE IN THE GAME
        add_pipe = False
        removed_pipes = []
        for pipe in pipes:
        # PIPES WILL MOVE ACROSS THE SCREEN (FROM RIGHT TO LEFT)
            pipe.move()

            # IF TOP/BOTTOM PIPE HITS BIRD, THE GAME WILL BE OVER
            if pipe.pipes_surface_bottom_rect.colliderect(bird.bird_surface_rect) or pipe.pipes_surface_top_rect.colliderect(bird.bird_surface_rect):
                run = False
                print('Game Over')

            if pipe.pipe_passed == False and pipe.pipes_surface_bottom_rect.centerx < bird.x:
                pipe.pipe_passed = True
                add_pipe = True

            # AND PIPES WILL BE REMOVED FROM GAME ONCE THEY MOVE LEFT OFF THE SCREEN
            if pipe.pipes_surface_bottom_rect.centerx < -50:
                removed_pipes.append(pipe)

        # NEW PIPE IS MOVE ACROSS SCREEN AND SCORE INCREASED BY ONE
        if add_pipe:
            score += 1
            pipes.append(Pipes())
        
        removed_pipes.clear()

        # IF BIRD HITS FLOOR OR CEILING, THE GAME WILL END
        if bird.bird_surface_rect.centery >= 620 or bird.bird_surface_rect.centery <= -10:
            run = False
            print('Game Over!')

        # MOVES FLOOR
        floor.move()

        # APPLIES GRAVITY TO BIRD
        bird.move() 
       
        # PUTS IMAGES IN GAME
        draw_screen(win, floor, pipes, bird, score)


main()

# LOADS NEAT CONFIG FILE
# def run(config_path):
#     config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

#     p = neat.Population(config)

#     p.add_reporter(neat.StdOutReporter(True))
#     stats = neat.StatisticsReporter()
#     p.add_reporter(stats)

#     winner = p.run(main, 50)

# if __name__ == '__main__':
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, 'config-feedforward.txt')
#     run(config_path)