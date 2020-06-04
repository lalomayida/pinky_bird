import pygame
import os
import time
import neat
import visualize
import pickle

from objects.bird import *
from objects.tube import *
from objects.base import *

pygame.font.init()
programIcon = pygame.image.load('images/bird2.png')

pygame.display.set_icon(programIcon)
pygame.display.set_caption("AI Pinky Bird")

sfont = pygame.font.SysFont("centurygothic", 30)
efont = pygame.font.SysFont("centurygothic", 70)

floor = 730
drawL = False

background_image = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "background.png")).convert_alpha(), (600, 900))

gen = 0


def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    if(gen == 0):
        gen = 1
    win.blit(background_image, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        if(drawL):
            try:
                pygame.draw.line(win, (255, 0, 0), (bird.x+bird.image.get_width()/2, bird.y + bird.image.get_height(
                )/2), (pipes[pipe_ind].x + pipes[pipe_ind].top_tube_image.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255, 0, 0), (bird.x+bird.image.get_width()/2, bird.y + bird.image.get_height(
                )/2), (pipes[pipe_ind].x + pipes[pipe_ind].bottom_tube_image.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        bird.draw(win)

    gen_label = sfont.render("GENERATION: " + str(gen-1), 1, (255, 255, 255))
    win.blit(gen_label, (10, 10))

    live_label = sfont.render("LIVE: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(live_label, (10, 40))

    point_label = sfont.render("POINTS: " + str(score), 1, (255, 255, 255))
    win.blit(point_label, (10, 70))

    pygame.display.update()


def main(genomes, config):
    global win_message, gen
    win = win_message
    gen += 1
    netsArray = []
    birdArray = []
    genomeArray = []

    #Setting Neural Network for each of the birds that we are running
    for ge_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config) 
        netsArray.append(net)
        birdArray.append(Bird(230, 350))
        genomeArray.append(genome)

    base = Base(floor)
    pipes = [Tube(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birdArray) > 0:
        clock.tick(2000)

        for event in pygame.event.get():
            #If we close the game manually
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0

        #Tagging the closestpipe in screen to be the one affecting the bird 
        if(len(birdArray) > 0):
            if(len(pipes) > 1 and birdArray[0].x > pipes[0].x + pipes[0].top_tube_image.get_width()):
                pipe_ind = 1
        
        # Deciding weather the bird wil jump or not  
        for x, bird in enumerate(birdArray):
            genomeArray[x].fitness += 0.1
            bird.move()
            output = netsArray[birdArray.index(bird)].activate((bird.y, abs(
                bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if(output[0] > 0.5):
                bird.jump()

        base.move()

        remove = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()

            for bird in birdArray:
                if(pipe.tocuhing(bird, win)):
                    genomeArray[birdArray.index(bird)].fitness -= 1
                    netsArray.pop(birdArray.index(bird))
                    genomeArray.pop(birdArray.index(bird))
                    birdArray.pop(birdArray.index(bird))

            if(pipe.x + pipe.top_tube_image.get_width() < 0):
                remove.append(pipe)

            if(not pipe.passed and pipe.x < bird.x):
                pipe.passed = True
                add_pipe = True

        if(add_pipe):
            score += 1
            
            # Adding fitness to a bird 
            for genome in genomeArray:
                genome.fitness += 5
            pipes.append(Tube(window_width))

        for r in remove:
            pipes.remove(r)

        for bird in birdArray:
            if(bird.y + bird.image.get_height() - 10 >= floor or bird.y < -50): # If the bird touches the ground
                netsArray.pop(birdArray.index(bird))
                genomeArray.pop(birdArray.index(bird))
                birdArray.pop(birdArray.index(bird))

        draw_window(win_message, birdArray, pipes, base, score, gen, pipe_ind)


def run(config_file):
    # The variables that are passed to Config() are the ones in the neat-config.txt file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    p = neat.Population(config)
    
    # Setting statistic reporter or the output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main)
    print('\nBest generation:\n{!s}'.format(winner))


if(__name__ == '__main__'):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)
