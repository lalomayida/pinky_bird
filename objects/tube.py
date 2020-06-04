import pygame
import os
import random

window_width = 600
window_height = 800

win_message = pygame.display.set_mode((window_width, window_height))
tube_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "tube.png")).convert_alpha())

class Tube():
    space = 200
    move_speed = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.top_tube_image = pygame.transform.flip(tube_image, False, True)
        self.bottom_tube_image = tube_image
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.top_tube_image.get_height()
        self.bottom = self.height + self.space

    def move(self):
        self.x -= self.move_speed

    def draw(self, win):
        win.blit(self.top_tube_image, (self.x, self.top))
        win.blit(self.bottom_tube_image, (self.x, self.bottom))

    def tocuhing(self, bird, win):
        bird_mask = bird.get_mask()
        top_tube_mask = pygame.mask.from_surface(self.top_tube_image)
        bottom_tube_mask = pygame.mask.from_surface(self.bottom_tube_image)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_tube_mask, bottom_offset)
        top_point = bird_mask.overlap(top_tube_mask, top_offset)

        if(bottom_point or top_point):
            return True

        return False
