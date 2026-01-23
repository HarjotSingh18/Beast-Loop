import pygame
pygame.mixer.init()


hit_sound = pygame.mixer.Sound("loopgame.py/sound/hurt_sound.mp3")
hit_sound.set_volume(0.1)

death_sound = pygame.mixer.Sound("loopgame.py/sound/death_sound.mp3")
death_sound.set_volume(0.5)

gun_sound = pygame.mixer.Sound("loopgame.py/sound/Wizard_Sound.mp3")
gun_sound.set_volume(15)

coin_sound = pygame.mixer.Sound("loopgame.py/sound/coin_pick.wav")
coin_sound.set_volume(0.2)