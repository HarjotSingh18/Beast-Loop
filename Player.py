import pygame
import math

from Sounds import *
from Weapons import *

pygame.mixer.init()

#! Player
PS = pygame.transform.smoothscale(pygame.image.load("images/player/wiz_1.png"), (80, 80))
PS_RECT = PS.get_rect(topleft = [90, 400])
PS_MASK = pygame.mask.from_surface(PS)

hit_sound = pygame.mixer.Sound("sound/hurt_sound.mp3")
hit_sound.set_volume(0.1)

death_sound = pygame.mixer.Sound("sound/death_sound.mp3")
death_sound.set_volume(0.5)
gun_sound = pygame.mixer.Sound("sound/Wizard_Sound.mp3")
gun_sound.set_volume(15)

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, health_width):
        super().__init__()
        
        #* Player Animation lists 
        self.idle = []
        self.hit = []
        self.dead = []
        self.health_width = health_width
        #* Player Animations
        img = pygame.image.load(f"images/player/wiz_1.png")
        img = pygame.transform.scale(img, (180, 180))
        self.idle.append(img)
    
        for num in range(1, 12):
            img = pygame.image.load(f"images/player/wiz_{num}.png")
            img = pygame.transform.scale(img, (180, 180))
            self.hit.append(img)

        #* Player indexes
        self.idle_index = 0
        self.hit_index = 0
        self.death_index = 0

        self.player_health = 10
        self.image = self.idle[self.idle_index]
        self.rect = self.image.get_rect(center = (x, y))
        self.mask = pygame.mask.from_surface(img)
        
        self.state = 'idle'

        #* Player counters
        self.idle_counter = 0   
        self.hit_counter = 0
        self.death_counter = 0

        #* Health bar width
        self.health_bar_width = health_width  # Initial width of health bar
        self.health_max_width = health_width  # Max health bar width, used to calculate the scale
        
        #* Player Weapon
        self.damage = 4
        self.damage_multiplier = 1

        #* Player coins 
        self.coins = 0

    def update(self):
        
        #! the higher the animation speed, the slower the animation
        hit_animation_speed = 7
        self.hit_counter += 1

        if self.state == "idle":
            self.image = self.idle[self.idle_index]


        if self.state == "hitting" and self.hit_counter >= hit_animation_speed and self.hit_index < len(self.hit) - 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
     
            self.hit_counter = 0
            self.hit_index += 1
            bullet = PlayerBullet(staff_rect.x, staff_rect.y, mouse_x, mouse_y, self.damage * self.damage_multiplier)
            if self.hit_index == 7:
                bullet_group.add(bullet)   
                gun_sound.play()
            self.image = self.hit[self.hit_index]

        if self.hit_index >= len(self.hit) - 1 and self.hit_counter >= hit_animation_speed:
        
            self.state = "idle"
            self.hit_index = 0       
                    
player_group = pygame.sprite.Group()
