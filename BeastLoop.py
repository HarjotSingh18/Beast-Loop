import pygame 
import math
import random
import time
import sys

from Enemies import *
from SmokeAnimation import *
from Particles import *
from FallingLeaves import *

pygame.font.init()

#! Window Attributes
WIDTH, HEIGHT = 1000,562
P_WIDTH, P_HEIGHT = 20,20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time Loop Defence")

#! Menu 
menu_1 = pygame.transform.smoothscale(pygame.image.load("images/menu/Menu_board.png"), (200 * 1.5, HEIGHT//2 * 1.5))
insturction = pygame.transform.smoothscale(pygame.image.load("images/menu/Instruction_menu.png"), (200 * 1.5, HEIGHT//2 * 1.5))

play_button = pygame.transform.smoothscale(pygame.image.load("images/menu/Play_Button.png"), (100, 70))
play_rect = play_button.get_rect(topleft = [250,100])

quit_button = pygame.transform.smoothscale(pygame.image.load("images/menu/Quit_Button.png"), (100, 70))
quit_rect = quit_button.get_rect(topleft = [400,100])

help_button = pygame.transform.smoothscale(pygame.image.load("images/menu/Help_Button.png"), (100, 70))
help_rect = help_button.get_rect(topleft = [550,100])

back_button = pygame.transform.smoothscale(pygame.image.load("images/menu/Back_Button.png"), (80, 50))
back_rect = back_button.get_rect(topleft = [435, 370])

#! Player GUI
health_x = 80
health_y = 10

health_bar_img = pygame.image.load("images/GUI/health_bar.png")

coin_Bar = pygame.transform.smoothscale(pygame.image.load("images/GUI/coin_gui.png"), (200, 70))
coin_Bar_rect = coin_Bar.get_rect(topleft = [0, 30])

my_font = pygame.font.SysFont('Comic Sans MS', 15)
coins_font = pygame.font.SysFont('Comic Sans MS', 35)

power_upgrade = pygame.transform.smoothscale(pygame.image.load("images/player/upgrades/power.png"), (28, 30))
power_rect = power_upgrade.get_rect(topleft = [10, 110])

health_upgrade = pygame.transform.smoothscale(pygame.image.load("images/player/upgrades/health_plus.png"), (30, 30))
health_upgrade_rect = health_upgrade.get_rect(topleft = [10, 150])

#! Location 1 
Location_1 = pygame.transform.smoothscale(pygame.image.load("images/location/background.png"), (WIDTH, HEIGHT)) 

#! Fps Attributes
clock = pygame.time.Clock()
fps = 60

#! Sounds
pygame.mixer.init()
background_music = pygame.mixer.Sound("sound/background music.mp3")
background_music.set_volume(0.5)
background_music.play(-1)

# Define enemy sets
def get_enemy_set(wave, cycle):
    enemies = []  # Initialize enemies as an empty list
    # First 2 waves (basic enemies)
    if wave < 6:
        enemies = [Mushroom(mushroom_rect.x, mushroom_rect.y, 1) for _ in range(1 + cycle)]  # Increase number of enemies as cycle increases
        enemies += [Boar(boar_rect.x, boar_rect.y, 2) for _ in range(1 + cycle)]
        enemies += [Dragon(bat_rect.x, bat_rect.y, 3) for _ in range(1 + cycle)]
    elif wave == 6:  # Boss wave
        enemies = [Orc(orc_rect.x, orc_rect.y, 20)]  # You can increase the boss's health or attributes if needed
    # elif wave > 6:
    #     enemis = 
    return enemies

def spawn_enemies(last_spawn, spawn_rate, enemy_tracker, enemies):
    # Enemies Spawn System
    if time.time() - last_spawn > spawn_rate:
        for enemy in enemies:
            # Spawn the enemy if not already spawned
            if not enemy.spawned:
                if isinstance(enemy, Mushroom):
                    mushroom_group.add(enemy)
                elif isinstance(enemy, Boar):
                    boar_group.add(enemy)
                elif isinstance(enemy, Dragon):
                    dragon_group.add(enemy)
                elif isinstance(enemy, Orc):
                    orc_group.add(enemy)
                enemy.spawned = True  # Mark the enemy as spawned
                last_spawn = time.time()
                enemy_tracker += 1
                break  # Spawn only one enemy per tick

        # Check if any enemies are dead and remove them
        for enemy in enemies[:]:  # Iterate over a copy of the list
            if enemy.health <= 0:  # If the enemy is dead, remove it
                enemies.remove(enemy)  # Remove the dead enemy from the list

    return last_spawn, enemies

leaf_animation = [pygame.transform.scale(pygame.image.load(f"images/location/leaves/lf_{i}.png"), (10, 10)) for i in range(1, 6)]
leaf_spawn_rate = 1.5  # Spawn new leaves every 1.5 seconds
last_leaf_time = time.time()

def draw_health_bar(player):
    health_gui = pygame.transform.smoothscale(health_bar_img, (player.health_bar_width, health_y))
    health_rect = health_gui.get_rect(topleft=[20, 390])
    WIN.blit(health_gui, health_rect)

def draw_coin_bar(player):
    coins = coins_font.render(f"{player.coins}", 1, "white")
    WIN.blit(coin_Bar, coin_Bar_rect)
    WIN.blit(coins, (80, 38))

def draw_leaves():
    global last_leaf_time
    # Spawn rate check for the leaves
    if time.time() - last_leaf_time > leaf_spawn_rate:
        x = random.randint(0, WIDTH)
        leaves = Leaves(x, 0, leaf_animation)
        leaves_group.add(leaves)
        last_leaf_time = time.time()  # Reset the last leaf spawn time

    # Update and draw leaves
    leaves_group.update()
    leaves_group.draw(WIN)

def draw_enemies():
    enemy_groups = [mushroom_group, boar_group, dragon_group, orc_group, coin_group, drop_group]
    
    # Update and draw each enemy group
    for player in player_group:
        for group in enemy_groups:
            group.update(player)
            group.draw(WIN)

def draw_others():
    bullet_group.update()
    bullet_group.draw(WIN)

    smoke_group.update()
    smoke_group.draw(WIN)

    player_group.update()
    player_group.draw(WIN)

def draw_upgrades():
    WIN.blit(power_upgrade, power_rect)
    WIN.blit(health_upgrade, health_upgrade_rect)

def draw(fps_text):
    player = list(player_group)[0]  # Assuming only one player
    
    # Load and draw map
    WIN.blit(Location_1, (0, 0))

    # Draw individual components
    draw_health_bar(player)
    draw_coin_bar(player)
    draw_leaves()
    draw_enemies()
    draw_others()
 

    # Draw FPS
    WIN.blit(fps_text, (10, 10))


def main():
    player_group.empty()
    mushroom_group.empty()
    boar_group.empty()
    dragon_group.empty()
    orc_group.empty()
    coin_group.empty()
    drop_group.empty()
    bullet_group.empty()
    leaves_group.empty()
    smoke_group.empty()
    smoke_group.add(smoke)  # The smoke sprite is created once on import, so re-add it after clearing
    run = True
    last_bullet_time = time.time()
    fire_Rate = 0.3

    player = Player(PS_RECT.x, PS_RECT.y, health_x)
    player_group.add(player)
    
    last_spawn = time.time()
    spawn_rate = 3
    enemy_tracker = 0
    wave = 2
    cycle = 0  # New variable to track the wave cycle
    enemies = get_enemy_set(wave, cycle)

    # [loc, velocity, timer]
    particles = []
    # Time variables for controlling particle spawn rate
    last_particle_time = 0
    particle_rate = 4 # Time (in seconds) between particle spawns

    while run:
        clock.tick(fps)
        
        idk = str(int(clock.get_fps()))
        fps_text = my_font.render(f"FPS: {idk}s", 1, "white")

        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                quit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and time.time() - last_bullet_time > fire_Rate:
                    for player in player_group:
                        player.state = "hitting"
                    last_bullet_time = time.time()

        # Wave system
        if len(enemies) == 0:

            wave += 1
            cycle += 1  # Increase the cycle for difficulty scaling
            spawn_rate -= 0.5
            enemies = get_enemy_set(wave, cycle)

            if len(enemies) == 0:  # If no enemies are returned, stop the wave progression
                #! Change it so that once wave ends, it goes into an upgrade function where 
                #! the player can spend there coins.
                print("No more enemies. Game over!")
                return
            else:
                print(f"New wave has {len(enemies)} enemies")
                
        last_spawn, enemies = spawn_enemies(last_spawn, spawn_rate, enemy_tracker, enemies)

        # Player death
        if player.player_health <= 0:
            print("You died. Game over!")
            return

        draw(fps_text)
        last_particle_time = particle(WIN, WIDTH, HEIGHT, particles, last_particle_time, particle_rate)
        pygame.display.update()

def quit_game():
    pygame.quit()
    sys.exit()

def menu():
    while True:
        clock.tick(fps)
        WIN.blit(Location_1, (0,0))
        WIN.blit(play_button, (250, 100))
        WIN.blit(quit_button, (400, 100))
        WIN.blit(help_button, (550, 100))
        pygame.display.update()

        mouse_Pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Use pygame.QUIT to check for the quit event
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if help_rect.collidepoint(mouse_Pos):
                    help()
                elif play_rect.collidepoint(mouse_Pos):  # Check if the mouse is within the start button rect
                    main()
                elif quit_rect.collidepoint(mouse_Pos):  # Check if the mouse is within the exit button rect
                    quit_game()

def help():
    while True:
        clock.tick(fps)
        WIN.blit(Location_1, (0,0))
        WIN.blit(insturction, (330, 50))
        WIN.blit(back_button, (435, 370))
        pygame.display.update()

        mouse_Pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Use pygame.QUIT to check for the quit event
                quit_game()
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(mouse_Pos):
                    return  # Back to the menu loop that opened this screen

def shop():
    pass

if __name__ == "__main__":
    menu()