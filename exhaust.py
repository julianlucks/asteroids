import pygame
import random
import math
from constants import *

class ExhaustParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed_multiplier=1.0):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        
        # Add some randomness to the direction and speed
        angle_variation = random.uniform(-0.3, 0.3)
        speed_variation = random.uniform(0.8, 1.2)
        
        # Calculate velocity opposite to the ship's direction
        direction_vector = pygame.Vector2(0, 1).rotate(direction + 180)  # Opposite direction
        direction_vector = direction_vector.rotate(angle_variation * 45)  # Add more spread
        self.velocity = direction_vector * EXHAUST_PARTICLE_SPEED * speed_variation * speed_multiplier
        
        self.lifetime = EXHAUST_PARTICLE_LIFETIME
        self.max_lifetime = EXHAUST_PARTICLE_LIFETIME
        self.initial_size = EXHAUST_PARTICLE_SIZE
        self.size = self.initial_size
        
        # Initialize color with full alpha
        self.color = (*EXHAUST_COLOR[:3], 255)
        
        # Quick fade settings
        self.quick_fade = False
        self.quick_fade_speed = 8.0  # Much faster fade
        self.quick_fade_time = 0.0

    def update(self, dt):
        if self.quick_fade:
            # Much faster lifetime reduction during quick fade
            self.lifetime -= dt * 6.0
        else:
            self.lifetime -= dt
            
        if self.lifetime <= 0:
            self.kill()
            return

        # Update position
        self.position += self.velocity * dt
        
        # Fade out and shrink over time
        life_fraction = self.lifetime / self.max_lifetime
        self.size = self.initial_size * life_fraction  # Shrink more aggressively
        
        # Calculate alpha with quick fade consideration
        base_alpha = int(255 * life_fraction)
        if self.quick_fade:
            base_alpha = int(base_alpha * 0.5)  # Immediately reduce alpha by half when stunned
        
        # Fade to regular orange
        self.color = (*EXHAUST_COLOR[:3], base_alpha)

    def draw(self, screen):
        if self.size < 1:
            return
            
        # Create a surface with alpha channel for fading
        size = max(1, int(self.size * 2))
        particle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, self.color, (size//2, size//2), max(1, self.size))
        screen.blit(particle_surface, (int(self.position.x - size//2), int(self.position.y - size//2)))

class ExhaustSystem(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.spawn_timer = 0
        
    def trigger_quick_fade(self):
        # Make all existing particles fade out quickly
        for particle in self.sprites():
            particle.quick_fade = True
        
    def update(self, dt, x, y, direction, is_moving, speed_multiplier=1.0):
        # Update existing particles
        for particle in self.sprites():
            particle.update(dt)
            
        # Only spawn new particles if moving and not quick fading
        if is_moving and not any(p.quick_fade for p in self.sprites()):
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn_timer = EXHAUST_SPAWN_RATE
                # Calculate spawn position at the back of the ship
                offset = -pygame.Vector2(0, PLAYER_RADIUS * 0.8).rotate(direction)  # Slightly inside the ship
                spawn_pos = pygame.Vector2(x, y) + offset
                # Spawn multiple particles for a fuller effect
                for _ in range(2):
                    self.add(ExhaustParticle(spawn_pos.x, spawn_pos.y, direction, speed_multiplier))
    
    def draw(self, screen):
        for particle in self.sprites():
            particle.draw(screen)
