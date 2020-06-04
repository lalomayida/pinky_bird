import pygame
import os

bird_images = [pygame.transform.scale2x(pygame.image.load(
    os.path.join("images", "bird" + str(x) + ".png"))) for x in range(1, 4)]

class Bird:
    top_rot = 25
    image_array = bird_images
    rotation_speed = 20
    animation_miliseconds = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = self.y
        self.image = self.image_array[0]
        self.clock_count = 0
        self.rotation = 0
        self.velocity = 0
        self.img_count = 0

    def jump(self):
        self.velocity = -10.5
        self.clock_count = 0
        self.height = self.y

    def move(self):
        self.clock_count += 1
        movement = self.velocity*(self.clock_count) + 1.5*(3)*(self.clock_count)**2
        if( movement >= 16):
            movement = (movement/abs(movement)) * 16

        if( movement < 0):
            movement -= 2

        self.y = self.y + movement

        if( movement < 0 or self.y < self.height + 50):
            if( self.rotation < self.top_rot):
                self.rotation = self.top_rot
        else:
            if( self.rotation > -90):
                self.rotation -= self.rotation_speed

    def draw(self, win):
        self.img_count += 1
        if( self.img_count <= self.animation_miliseconds):
            self.image = self.image_array[0]
        elif self.img_count <= self.animation_miliseconds*2:
            self.image = self.image_array[1]
        elif self.img_count <= self.animation_miliseconds*3:
            self.image = self.image_array[2]
        elif self.img_count <= self.animation_miliseconds*4:
            self.image = self.image_array[1]
        elif self.img_count == self.animation_miliseconds*4 + 1:
            self.image = self.image_array[0]
            self.img_count = 0

        if( self.rotation <= -80):
            self.image = self.image_array[1]
            self.img_count = self.animation_miliseconds*2

        blitRotateCenter(win, self.image, (self.x, self.y), self.rotation)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
