from circleshape import CircleShape 
from constants import *
from explosion import Explosion
import pygame
import random
import math

class Asteroid(CircleShape):
    containers = None

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-90, 90)  # Degrees per second
        
        # Generate points for lumpy shape
        self.num_points = random.randint(ASTEROID_MIN_POINTS, ASTEROID_MAX_POINTS)
        self.variations = []
        for _ in range(self.num_points):
            variation = random.uniform(ASTEROID_MIN_VARIATION, ASTEROID_MAX_VARIATION)
            self.variations.append(variation)
        
        # Generate random crater positions
        self.craters = []
        for _ in range(ASTEROID_CRATER_COUNT):
            angle = random.uniform(0, 360)
            distance = random.uniform(0.2, 0.8) * radius
            crater_radius = random.uniform(0.2, 0.4) * radius
            self.craters.append((angle, distance, crater_radius))
        
        # Generate surface noise points
        self.noise_points = []
        noise_count = int(radius / 3)  # Scale noise points with asteroid size
        for _ in range(noise_count):
            angle = random.uniform(0, 360)
            distance = random.uniform(0.8, 1.0) * radius
            size = random.uniform(2, 4)
            self.noise_points.append((angle, distance, size))

    def get_lumpy_points(self):
        points = []
        for i in range(self.num_points):
            angle = math.radians(360 / self.num_points * i + self.rotation)
            distance = self.radius * self.variations[i]
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance
            points.append((x, y))
        return points

    def update(self, dt):
        # Update position
        self.position += self.velocity * dt
        self.wrap_position()
        # Update rotation
        self.rotation += self.rotation_speed * dt

    def wrap_position(self):
        """Wrap the asteroid's position around screen edges"""
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def draw(self, screen):
        # Create a surface for the asteroid with alpha channel
        surface_size = int(self.radius * 2.8)  # Larger to accommodate lumpy shape
        surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        center = (surface_size // 2, surface_size // 2)
        
        # Get lumpy shape points
        shape_points = self.get_lumpy_points()
        screen_points = [(int(x + center[0]), int(y + center[1])) for x, y in shape_points]
        
        # Draw base lumpy asteroid shape
        pygame.draw.polygon(surface, ASTEROID_BASE_COLOR, screen_points, 0)
        
        # Create a clip mask for the lumpy shape
        mask_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        pygame.draw.polygon(mask_surface, (255, 255, 255, 255), screen_points, 0)
        
        # Draw craters
        for angle, distance, crater_radius in self.craters:
            # Rotate crater position
            rotated_angle = math.radians(angle + self.rotation)
            crater_x = center[0] + math.cos(rotated_angle) * distance
            crater_y = center[1] + math.sin(rotated_angle) * distance
            
            # Draw crater shadow (slightly offset)
            shadow_offset = crater_radius * 0.2
            shadow_pos = (crater_x + shadow_offset, crater_y + shadow_offset)
            pygame.draw.circle(surface, ASTEROID_CRATER_COLOR, 
                            (int(shadow_pos[0]), int(shadow_pos[1])), 
                            int(crater_radius))
            
            # Draw crater
            pygame.draw.circle(surface, ASTEROID_CRATER_COLOR, 
                            (int(crater_x), int(crater_y)), 
                            int(crater_radius))
        
        # Draw surface noise (small bumps and highlights)
        for angle, distance, size in self.noise_points:
            # Rotate noise position
            rotated_angle = math.radians(angle + self.rotation)
            noise_x = center[0] + math.cos(rotated_angle) * distance
            noise_y = center[1] + math.sin(rotated_angle) * distance
            
            # Draw highlight
            highlight_pos = (int(noise_x - size/4), int(noise_y - size/4))
            pygame.draw.circle(surface, ASTEROID_HIGHLIGHT_COLOR, highlight_pos, int(size))
            
            # Draw shadow
            shadow_pos = (int(noise_x + size/4), int(noise_y + size/4))
            pygame.draw.circle(surface, ASTEROID_CRATER_COLOR, shadow_pos, int(size))
        
        # Apply the clip mask
        surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Draw outline
        pygame.draw.polygon(surface, (255, 255, 255), screen_points, 1)
        
        # Blit the asteroid surface onto the screen
        screen_pos = (int(self.position.x - surface_size//2),
                     int(self.position.y - surface_size//2))
        screen.blit(surface, screen_pos)

    def split(self):
        # Create explosion effect
        Explosion(self.position.x, self.position.y, color=(255, 200, 100))
        
        # If the asteroid is too small, just remove it
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
            return
            
        # Create two smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Generate random angles for the new velocities
        split_angle = random.uniform(20, 50)
        velocity1 = self.velocity.rotate(split_angle) * 1.2
        velocity2 = self.velocity.rotate(-split_angle) * 1.2
        
        # Create the new asteroids
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = velocity1
        
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = velocity2
        
        # Add them to the sprite groups
        if self.containers:
            for group in self.containers:
                group.add(asteroid1)
                group.add(asteroid2)
        
        # Remove the original asteroid
        self.kill()