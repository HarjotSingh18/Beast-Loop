import pygame
from Sounds import *
from Player import *

class EnemyDrop(pygame.sprite.Sprite):
    def __init__(self, x, y, drop_animation, drop_val):
        super().__init__()

        self.drop = drop_animation
        self.drop_val = drop_val
        self.drop_index = 0
        self.hover_over = False
        self.image = self.drop[self.drop_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.state = 'running'  # Can be 'running', 'hit', 'dead'

        # Animation counters
        self.drop_counter = 0

    def update(self, player):
        if self.rect.y < 450:
             self.rect.y += 1
        # Animation speeds
        drop_animation_speed = 10
        mouse_pos = pygame.mouse.get_pos()

        # Increment counters
        self.drop_counter += 1
            
        if self.drop_counter >= drop_animation_speed and self.drop_index < len(self.drop) - 1:
                self.drop_counter = 0
                self.drop_index += 1
                self.image = self.drop[self.drop_index]

        #if run animation is complete, reset animation index
        if self.drop_index >= len(self.drop) - 1 and self.drop_counter >= drop_animation_speed:
            self.drop_index = 0

        if self.rect.collidepoint(mouse_pos):
            coin_sound.play()
            player.coins += self.drop_val
            self.kill()

drop_group = pygame.sprite.Group()
