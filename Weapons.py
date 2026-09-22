import pygame
import math

#! Weapon Images 
staff = pygame.transform.smoothscale(pygame.image.load("images/weapons/Pistol-3.png"), (30, 30))
staff_rect = staff.get_rect(topleft = [70, 390])
staff_mask = pygame.mask.from_surface(staff)

bullet_1 = pygame.transform.smoothscale(pygame.image.load("images/weapons/simple_bullet.png"), (10, 10))
bullet_1_rect = staff.get_rect(topleft = [0,0])
bullet_1_mask = pygame.mask.from_surface(bullet_1)
BULLET_VEL = 2
BULLET_1 = pygame.transform.smoothscale(pygame.image.load("images/weapons/Bullet_Wizzart_C.png"), (55, 55))

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y, damage):
        super().__init__()
        self.images = []
        self.images.append(BULLET_1)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = BULLET_1.get_rect(center = (x, y))
        self.mask = pygame.mask.from_surface(BULLET_1)
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.bullet_damge = damage

        self.speed = 15
       
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def update(self):
        self.rect.x -= int(self.x_vel)
        self.rect.y -= int(self.y_vel)

        # Remove bullets that have left the screen
        if not self.rect.colliderect(pygame.display.get_surface().get_rect()):
            self.kill()

bullet_group = pygame.sprite.Group()