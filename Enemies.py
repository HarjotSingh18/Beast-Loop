import pygame

from Sounds import *
from Player import *
from EnemyDrops import *

#! Enemies 
mushroom = pygame.transform.smoothscale(pygame.image.load("loopgame.py/images/enemies/mushroom/run/run_1.png"), (80, 80))
mushroom_rect = mushroom.get_rect(topleft = [950, 460])
mushroom_mask = pygame.mask.from_surface(mushroom)

boar = pygame.transform.smoothscale(pygame.image.load("loopgame.py/images/enemies/boar/run/run_1.png"), (80, 80))
boar_rect = mushroom.get_rect(topleft = [950, 465])
boar_mask = pygame.mask.from_surface(mushroom)

bat = pygame.transform.smoothscale(pygame.image.load("loopgame.py/images/enemies/dragon/flying/fly_1.png"), (40,40))
bat_rect = bat.get_rect(topleft = [950, 300])
bat_mask = pygame.mask.from_surface(bat)

orc_boss = pygame.transform.smoothscale(pygame.image.load("loopgame.py/images/enemies/orc_boss/run/run_1.png"), (80,80))
orc_rect = orc_boss.get_rect(topleft = [950, 420])
orc_mask = pygame.mask.from_surface(orc_boss)

#! Enemies Drops 
coin_drop = pygame.transform.smoothscale(pygame.image.load("loopgame.py/images/GUI/coins/coin_1.png"), (80, 80))
coin_drop_rect = coin_drop.get_rect(topleft = [0,0])
coin_drop_mask = pygame.mask.from_surface(coin_drop)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, run_animation, hit_animation, death_animation,attack_animation , run_speed, coin_drop):
        super().__init__()

        # Animation lists
        self.run = run_animation
        self.hit = hit_animation or []
        self.death = death_animation or []
        self.attack = attack_animation or []
        self.coin_val = coin_drop
        # Indexes for animations
        self.run_index = 0
        self.hit_index = 0
        self.death_index = 0
        self.attack_index = 0

        self.health = health
        self.image = self.run[self.run_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.spawned = False
        self.state = 'running'  # Can be 'running', 'hit', 'dead'
        self.run_speed = run_speed

        # Animation counters
        self.run_counter = 0
        self.hit_counter = 0
        self.death_counter = 0
        self.attack_counter = 0

    def update(self, player):
        if self.state != "dead":
            self.rect.x -= self.run_speed  # Move enemy left

        # Animation speeds
        run_animation_speed = 10
        hit_animation_speed = 8
        death_animation_speed = 9
        attack_animation_speed = 10

        # Increment counters
        self.run_counter += 1
        self.hit_counter += 1
        self.death_counter += 1
        self.attack_counter += 1
            
        if self.state == "running" and self.run_counter >= run_animation_speed and self.run_index < len(self.run) - 1:
                self.run_counter = 0
                self.run_index += 1
                self.image = self.run[self.run_index]

        if self.state == "hit" and self.hit_counter >= hit_animation_speed and self.hit_index < len(self.hit) - 1:
            self.hit_counter = 0
            self.hit_index += 1        
            self.image = self.hit[self.hit_index]
        
        if self.state == "dead" and self.death_counter >= death_animation_speed and self.death_index < len(self.death) - 1:
            self.death_counter = 0
            self.death_index += 1        
            self.image = self.death[self.death_index]

        #if run animation is complete, reset animation index
        if self.run_index >= len(self.run) - 1 and self.run_counter >= run_animation_speed:
            self.run_index = 0

        # If hit animation is complete or doesn't exist, go back to running
        if self.state == "hit" and (not self.hit or self.hit_index >= len(self.hit) - 1):
            self.hit_index = 0
            self.state = "running"
        
        # Death animation (only if there is a death animation)
        if self.state == "dead" and self.death and self.death_counter >= death_animation_speed and self.death_index < len(self.death) - 1:
            self.death_counter = 0
            self.death_index += 1
            self.image = self.death[self.death_index]
            
        # If death animation is complete or doesn't exist, kill the enemy
        if self.state == "dead" and (not self.death or self.death_index >= len(self.death) - 1):
            self.kill()  # Remove the enemy sprite
                
        if PS_MASK.overlap(self.mask, (self.rect.x - PS_RECT.x, self.rect.y - PS_RECT.y)) and self.state != "dead":
            hit_sound.play()
            player.player_health -= 5  # Access the player's health
            self.health = 0
            self.kill()
            player.health_bar_width = player.health_bar_width * (player.player_health / 10)

        for bullet in bullet_group:
            bullet_mask = bullet.mask  # Access the mask of the current bullet
            bullet_rect = bullet.rect  # Access the rect of the current bullet
            
            if bullet_mask.overlap(self.mask, (self.rect.x - bullet_rect.x, self.rect.y - bullet_rect.y)) and self.state != "dead":
                bullet.kill()
                self.health -= bullet.bullet_damge

                if self.health <= 0:
                    death_sound.play()
                    self.state = "dead"
                    coin_animaton = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/GUI/coins/coin_{i}.png"), (40, 40)) for i in range(1, 6)]
                    drop = EnemyDrop(self.rect.x, self.rect.y, coin_animaton, self.coin_val)
                    drop_group.add(drop)
                else:
                    hit_sound.play()
                    self.state = "hit" 
# All enemies 
class Mushroom(Enemy):
    def __init__(self, x, y, health):
        run_animation = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/enemies/mushroom/run/run_{i}.png"), (70, 70)) for i in range(1, 9)]
        hit_animation = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/enemies/mushroom/hit/hit_{i}.png"), (70, 70)) for i in range(1, 5)]
        #! using death animation for the dragon because it looks nicer
        death_animation = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/enemies/mushroom/death/die_{i}.png"), (70,70)) for i in range(1,6)]
        self.coin_drop = 1
        super().__init__(x, y, health, run_animation, hit_animation, death_animation, None, 2, self.coin_drop)

class Boar(Enemy):
    def __init__(self, x, y, health):
        run_animation = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/enemies/boar/run/run_{i}.png"), (70, 60)) for i in range(1, 4)]
        death_animation = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/enemies/boar/death/dead_{i}.png"), (60, 60)) for i in range(1, 10)]
        self.coin_drop = 2      
        super().__init__(x, y, health, run_animation, None, death_animation, None, 2, self.coin_drop)

class Dragon(Enemy):
    def __init__(self, x, y, health):
        run_animation = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/enemies/dragon/flying/fly_{i}.png"), (100, 100)) for i in range(1, 10)]
        death_animation = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/enemies/dragon/death/dead_{i}.png"), (100,100)) for i in range(1,6)]
        self.coin_drop = 3     
        super().__init__(x, y, health, run_animation, None, death_animation, None, 2, self.coin_drop)

    def update(self, player):
        if self.rect.x < 160:  
            self.rect.y += 5  

        super().update(player)

class Orc(Enemy):
    def __init__(self, x, y, health):
        run_animation = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/enemies/orc_boss/run/run_{i}.png"), (150, 150)) for i in range(1, 9)]
        hit_animation = [pygame.transform.scale(pygame.image.load(f"loopgame.py/images/enemies/orc_boss/hit/hit_{i}.png"), (150, 150)) for i in range(1, 4)]
        self.coin_drop = 5
        super().__init__(x, y, health, run_animation, hit_animation, None, None, 1, self.coin_drop)  # Slower but more powerful boss

mushroom_group = pygame.sprite.Group()
boar_group = pygame.sprite.Group()
dragon_group = pygame.sprite.Group()
orc_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()