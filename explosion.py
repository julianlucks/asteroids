import pygame
import random
import math
from constants import *

class ExplosionParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, color=(255, 255, 255)):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.lifetime = EXPLOSION_PARTICLE_LIFETIME
        self.color = color
        self.size = EXPLOSION_PARTICLE_SIZE

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return

        # Update position
        self.position += self.velocity * dt
        
        # Fade out by adjusting color alpha based on remaining lifetime
        fade = self.lifetime / EXPLOSION_PARTICLE_LIFETIME
        self.color = (self.color[0], self.color[1], self.color[2], int(255 * fade))

    def draw(self, screen):
        # Create a surface with alpha channel for fading
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        alpha_color = (*self.color[:3], int(self.color[3] if len(self.color) > 3 else 255))
        pygame.draw.circle(particle_surface, alpha_color, (self.size, self.size), self.size)
        screen.blit(particle_surface, (int(self.position.x - self.size), int(self.position.y - self.size)))

class Explosion(pygame.sprite.Sprite):
    containers = None

    def __init__(self, x, y, color=(255, 255, 255)):
        if self.containers:
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.particles = pygame.sprite.Group()
        
        # Create particles in a circular pattern
        for i in range(EXPLOSION_PARTICLE_COUNT):
            angle = math.radians(360 / EXPLOSION_PARTICLE_COUNT * i)
            # Add some randomness to speed and angle
            speed = EXPLOSION_PARTICLE_SPEED * random.uniform(0.8, 1.2)
            angle += random.uniform(-0.2, 0.2)  # Small random angle variation
            
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            particle = ExplosionParticle(x, y, velocity, color)
            self.particles.add(particle)

    def update(self, dt):
        self.particles.update(dt)
        # Remove the explosion if all particles are gone
        if len(self.particles) == 0:
            self.kill()

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
