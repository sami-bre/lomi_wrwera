import random
import pygame



class BirdSprite(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        super().__init__()
        self.velocity = [random.randint(-5, 5)/1, random.randint(-5, 5)/1]
        self.images = [pygame.image.load(f'./{i}.gif') for i in range(0, 14, 2)]
        # resize the images
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (60, 60))
        self.current_image = 0
        self.image = self.images[self.current_image]
        if self.velocity[0] < 0:
            for i in range(len(self.images)):
                self.images[i] = pygame.transform.flip(self.images[i], True, False)
        self.rect = self.image.get_rect()  # Get the rect object for positioning
        self.rect.topleft = initial_position  # Set the initial position
        self.rect.width = 50
        self.rect.height = 50

    def update(self, window_dimensions):
        # update the image
        self.current_image = (self.current_image + 1) % (3*len(self.images))
        if(self.current_image % 3 == 0):
            self.image = self.images[int(self.current_image/3)]
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if(self.rect.x < window_dimensions[0][0] or self.rect.x > window_dimensions[0][1]):
            self.velocity[0] *= -1
            for i in range(len(self.images)):
                self.images[i] = pygame.transform.flip(self.images[i], True, False)
        if( self.rect.y < window_dimensions[1][0] or self.rect.y > window_dimensions[1][1]):
            self.velocity[1] *= -1

class AimSprite(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        super().__init__()
        self.image = pygame.image.load('./aim.png')  # Load the image
        self.rect = self.image.get_rect()  # Get the rect object for positioning
        self.rect.center = initial_position  # Set the initial position

    def update(self, mouse_position):
        self.rect.x += mouse_position[0]
        self.rect.y += mouse_position[1]



class StoneSprite(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        super().__init__()
        self.image = pygame.image.load('./stone.png')  # Load the image
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()  # Get the rect object for positioning
        self.rect.topleft = initial_position  # Set the initial position
        self.rect.width = 30
        self.rect.height = 30

