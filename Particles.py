import pygame
import time
import random

# Colors
WHITE = (255, 255, 255)
COLOR = (91, 44, 111)

# Create particle surface with glow
def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


def particle(WIN, WIDTH, HEIGHT, particles, last_particle_time, particle_rate):
    # Get current time
    current_time = pygame.time.get_ticks() / 1000  # Get time in seconds

    if current_time - last_particle_time > particle_rate:

    # Spawn new particles if enough time has passed
        for _ in range(1):  # Control how many particles spawn at each frame
            px = random.randint(0, WIDTH)  # Random X position along the top of the screen
            py = random.randint(0, HEIGHT//3)  # Y position set to 0 (ceiling)
            vx = random.uniform(-1, 1)  # Random horizontal velocity
            vy = 1  # Downward velocity
            size = 4  # Random size for the particles
            particles.append([[px, py], [vx, vy], size])
            
            last_particle_time = current_time
        
    # Update last spawn time

    # Update particles
    for particle in particles[:]:
        # Update position based on velocity
        particle[0][0] += particle[1][0]  # X position
        particle[0][1] += particle[1][1]  # Y position
        particle[2] -= 0.01  # Shrink particle over time

        # Draw the particle as a white circle
        pygame.draw.circle(WIN, WHITE, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

        # Draw particle glow with blend effect
        radius = particle[2] * 2
        WIN.blit(circle_surf(int(radius), COLOR), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pygame.BLEND_RGB_ADD)

        # Remove particle if it shrinks too much or falls off the screen
        if particle[2] <= 0 or particle[0][1] > 490:
            particles.remove(particle)

    return last_particle_time  # Return the updated spawn time
