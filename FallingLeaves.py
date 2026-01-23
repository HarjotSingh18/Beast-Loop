import pygame
import random

class Leaves(pygame.sprite.Sprite):
    def __init__(self, x, y, falling_animation):
        super().__init__()

        self.falling = falling_animation
        self.falling_index = 0
        self.image = self.falling[self.falling_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.state = 'falling'  # Can be 'running', 'hit', 'dead'

        # Animation counters
        self.falling_counter = 0

    def update(self):

        if self.rect.y < 490:
             self.rect.y += 1
             self.rect.x -= 1
        else:
             self.kill()
        # Animation speeds
        falling_animation_speed = 10

        # Increment counters
        self.falling_counter += 1
            
        if self.falling_counter >= falling_animation_speed and self.falling_index < len(self.falling) - 1:
                self.falling_counter = 0
                self.falling_index += 1
                self.image = self.falling[self.falling_index]

        if self.falling_index >= len(self.falling) - 1 and self.falling_counter >= falling_animation_speed:
            self.falling_index = 0


leaves_group = pygame.sprite.Group()
