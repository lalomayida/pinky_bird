import pygame
import os

base_image = pygame.transform.scale2x(pygame.image.load(
    os.path.join("images", "base.png")).convert_alpha())

class Base:
    base_width = base_image.get_width()
    base_image = base_image
    mode_speed = 5

    def __init__(self, y):
        self.y = y
        self.first_image_x_position = 0
        self.second_image_x_position = self.base_width

    def move(self):
        self.first_image_x_position -= self.mode_speed
        self.second_image_x_position -= self.mode_speed
        if( self.first_image_x_position + self.base_width < 0):
            self.first_image_x_position = self.second_image_x_position + self.base_width

        if( self.second_image_x_position + self.base_width < 0):
            self.second_image_x_position = self.first_image_x_position + self.base_width

    def draw(self, win):
        win.blit(self.base_image, (self.first_image_x_position, self.y))
        win.blit(self.base_image, (self.second_image_x_position, self.y))
