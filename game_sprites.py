import random
import pygame



class BirdSprite(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        super().__init__()
        self.velocity = [random.randint(-5, 5)/1, random.randint(-5, 5)/1]
        self.image = pygame.image.load('./bird.png')  # Load the image
        if self.velocity[0] < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()  # Get the rect object for positioning
        self.rect.topleft = initial_position  # Set the initial position
        self.rect.width = 50
        self.rect.height = 50

    def update(self, window_dimensions):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if(self.rect.x < window_dimensions[0][0] or self.rect.x > window_dimensions[0][1]):
            self.velocity[0] *= -1
            self.image = pygame.transform.flip(self.image, True, False)
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
        self.rect = self.image.get_rect()  # Get the rect object for positioning
        self.rect.topleft = initial_position  # Set the initial position
        self.rect.width = 50
        self.rect.height = 50

