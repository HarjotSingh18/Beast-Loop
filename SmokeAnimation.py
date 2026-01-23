import pygame

smk_img = pygame.transform.smoothscale(pygame.image.load("images/location/smoke/smk_1.png"), (80,80))
smk_rect = smk_img.get_rect(topleft = [0,0])


class Smoke(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.smk_Animation = [pygame.transform.scale(pygame.image.load(f"images/location/smoke/smk_{i}.png"), (80,80)) for i in range(1, 7)]
        self.smk_index = 0
        self.smk_counter = 0
        x,y = 370, 142

        self.image = self.smk_Animation[self.smk_index]
        self.rect = self.image.get_rect(center = (x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        smk_animation_Speed = 11
        self.smk_counter += 1

        if self.smk_counter >= smk_animation_Speed and self.smk_index < len(self.smk_Animation) - 1:
                self.smk_counter = 0
                self.smk_index += 1
                self.image = self.smk_Animation[self.smk_index]

        if self.smk_index >= len(self.smk_Animation) - 1 and self.smk_counter >= smk_animation_Speed:
            self.smk_index = 0

# Create the shop instance and add it to the shop_group
smoke_group = pygame.sprite.Group()
smoke = Smoke()
smoke_group.add(smoke)


