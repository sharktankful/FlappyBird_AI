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
game_font = pygame.font.SysFont('comicsans', 35)
white = (255, 255, 255)

# VARIBALE FOR GENERATIONS RUN
generation = 0

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
bird_flap = pygame.USEREVENT
pygame.time.set_timer(bird_flap, 100)


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
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

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

    def draw(self, win, pipes):
        rotate_bird = pygame.transform.rotozoom(
            self.bird_surface[self.flap_number], -self.movement * 3, 1)
        win.blit(rotate_bird, self.bird_surface_rect)
        pygame.draw.rect(win, self.color, (self.bird_surface_rect.x, self.bird_surface_rect.y, self.bird_surface_rect.width, self.bird_surface_rect.height), 2)

        for pipe in pipes:
            if pipe.pipes_surface_bottom_rect.x > self.bird_surface_rect.x:
                pygame.draw.line(win, self.color, (self.bird_surface_rect.x + 54, self.bird_surface_rect.y + 12), pipe.pipes_surface_bottom_rect.midtop, 2)
                pygame.draw.line(win, self.color, (self.bird_surface_rect.x + 54, self.bird_surface_rect.y + 12), pipe.pipes_surface_top_rect.midbottom, 2)


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
        self.height = random.randrange(300, 600)
        self.pipes_surface_bottom = pipes_surface
        self.pipes_surface_bottom_rect = self.pipes_surface_bottom.get_rect(
            midtop=(550, self.height))
        self.pipes_surface_top = pygame.transform.flip(
            pipes_surface, False, True)
        self.pipes_surface_top_rect = self.pipes_surface_top.get_rect(
            midbottom=(550, self.height - 200))

    def move(self):
        self.pipes_surface_bottom_rect.centerx -= 3
        self.pipes_surface_top_rect.centerx -= 3

    def draw(self, win):
        win.blit(self.pipes_surface_top, self.pipes_surface_top_rect)
        win.blit(self.pipes_surface_bottom, self.pipes_surface_bottom_rect)


# DRAWS OBJECTS/BACKGROUND IMAGES TO SCREEN
def draw_screen(win, floor, pipes, birds, score, generation):
    win.blit(bg_surface, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    floor.draw(win)

    for bird in birds:
        bird.draw(win, pipes)

    score_label = game_font.render(f'Score: {score}', 1, white)
    win.blit(score_label, (screen_width - score_label.get_width() - 15, 10))

    generation_label = game_font.render(f'Gen: {generation}', 1, white)
    win.blit(generation_label, (10, 10))

    pygame.display.update()


# MAIN GAME FUNCTION
def main(genomes, config):
    global generation

    # VARIABLES FOR NEURAL NETWORK
    generation += 1
    birds = []
    nets = []
    ge = []

    # FOR EACH AI, A NEURAL NETWORK, BIRD, AND GENOME WILL BE APPLIED
    for genome_id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        g.fitness = 0
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(g)

    # FUNCTION VARIABLES
    score = 0
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((screen_width, screen_height))
    floor = Floor()
    pipes = [Pipes()]

    # MAIN GAME LOOP
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit
                sys.exit()
            for bird in birds:
                if event.type == bird_flap:
                    bird.bird_animation()

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].pipes_surface_bottom_rect.centerx + pipes[0].pipes_surface_top.get_width():
                pipe_index = 1
        else:
            run == False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.bird_surface_rect.y, abs(
                bird.bird_surface_rect.y - pipes[pipe_index].height), abs(bird.bird_surface_rect.y - pipes[pipe_index].height - 200)))

            if output[0] > 0.5:
                bird.jump()

        # HOW PIPES WILL BEHAVE IN THE GAME
        add_pipe = False
        removed_pipes = []
        for pipe in pipes:
            # BIRD WILL BE REMOVED AND HAVE ITS FITNESS DECREASED BY ONE IF IT HITS A PIPE
            for x, bird in enumerate(birds):
                if pipe.pipes_surface_bottom_rect.colliderect(bird.bird_surface_rect) or pipe.pipes_surface_top_rect.colliderect(bird.bird_surface_rect):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.pipe_passed and pipe.pipes_surface_bottom_rect.centerx < bird.x:
                    pipe.pipe_passed = True
                    add_pipe = True

            # AND PIPES WILL BE REMOVED FROM GAME ONCE THEY MOVE LEFT OFF THE SCREEN
            if pipe.pipes_surface_bottom_rect.centerx < -50:
                removed_pipes.append(pipe)

            # PIPES WILL MOVE ACROSS THE SCREEN (FROM RIGHT TO LEFT)
            pipe.move()

        # NEW PIPE IS MOVED ACROSS SCREEN, SCORE INCREASED BY ONE, AND BIRD FITNESS INCREASED BY FIVE
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipes())

        # PASSED PIPES IS REMOVED
        for pipe in removed_pipes:
            pipes.remove(pipe)

        # IF BIRD HITS FLOOR OR CEILING, THE BIRD, NET, AND GE WILL BE DELETED
        for x, bird in enumerate(birds):
            if bird.bird_surface_rect.centery >= 620 or bird.bird_surface_rect.centery <= -10:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        # MOVES FLOOR
        floor.move()

        # PUTS IMAGES IN GAME
        draw_screen(win, floor, pipes, birds, score, generation)


# LOADS NEAT CONFIG FILE
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
