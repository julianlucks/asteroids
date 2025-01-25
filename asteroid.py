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
            height = random.uniform(0.5, 1.0)  # Relative height for lighting
            self.noise_points.append((angle, distance, size, height))

    def get_lumpy_points(self):
        points = []
        normals = []  # Store normal vectors for lighting
        for i in range(self.num_points):
            angle = math.radians(360 / self.num_points * i + self.rotation)
            distance = self.radius * self.variations[i]
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance
            points.append((x, y))
            # Calculate normal vector for this point
            normal = pygame.Vector2(x, y).normalize()
            normals.append(normal)
        return points, normals

    def get_lighting_factor(self, normal, height_modifier=0):
        # Normalize light direction
        light_dir = LIGHT_DIRECTION.normalize()
        # Calculate dot product between normal and light direction
        dot_product = normal.dot(light_dir)
        # Adjust for height modifier (for bumps and craters)
        dot_product += height_modifier
        # Clamp between ambient light and max intensity
        lighting = AMBIENT_LIGHT + (1 - AMBIENT_LIGHT) * max(0, min(1, dot_product))
        return lighting

    def apply_lighting(self, color, lighting_factor):
        # Apply lighting to color
        lit_color = [int(c * lighting_factor) for c in color[:3]]
        return (*lit_color, color[3] if len(color) > 3 else 255)

    def draw(self, screen):
        # Create a surface for the asteroid with alpha channel
        surface_size = int(self.radius * 2.8)  # Larger to accommodate lumpy shape
        surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        center = (surface_size // 2, surface_size // 2)
        
        # Get lumpy shape points and normals
        shape_points, shape_normals = self.get_lumpy_points()
        screen_points = [(int(x + center[0]), int(y + center[1])) for x, y in shape_points]
        
        # Create base polygon surface
        base_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        
        # Draw base shape with lighting
        for i, (point, normal) in enumerate(zip(screen_points, shape_normals)):
            next_point = screen_points[(i + 1) % len(screen_points)]
            # Create a triangle with the center and two adjacent points
            triangle = [center, point, next_point]
            # Get lighting for this face
            lighting = self.get_lighting_factor(normal)
            color = self.apply_lighting(ASTEROID_BASE_COLOR, lighting)
            pygame.draw.polygon(base_surface, color, triangle)
        
        # Draw craters with lighting
        for angle, distance, crater_radius in self.craters:
            # Rotate crater position
            rotated_angle = math.radians(angle + self.rotation)
            crater_x = center[0] + math.cos(rotated_angle) * distance
            crater_y = center[1] + math.sin(rotated_angle) * distance
            
            # Calculate crater normal (pointing slightly inward)
            crater_normal = pygame.Vector2(math.cos(rotated_angle), math.sin(rotated_angle))
            lighting = self.get_lighting_factor(crater_normal, -CRATER_DEPTH)
            crater_color = self.apply_lighting(ASTEROID_CRATER_COLOR, lighting)
            
            # Draw crater
            pygame.draw.circle(base_surface, crater_color, 
                            (int(crater_x), int(crater_y)), 
                            int(crater_radius))
        
        # Draw surface bumps with lighting
        for angle, distance, size, height in self.noise_points:
            # Rotate bump position
            rotated_angle = math.radians(angle + self.rotation)
            bump_x = center[0] + math.cos(rotated_angle) * distance
            bump_y = center[1] + math.sin(rotated_angle) * distance
            
            # Calculate bump normal (pointing outward)
            bump_normal = pygame.Vector2(math.cos(rotated_angle), math.sin(rotated_angle))
            lighting = self.get_lighting_factor(bump_normal, BUMP_HEIGHT * height)
            highlight_color = self.apply_lighting(ASTEROID_HIGHLIGHT_COLOR, lighting)
            
            # Draw the bump
            pygame.draw.circle(base_surface, highlight_color,
                            (int(bump_x), int(bump_y)),
                            int(size))
        
        # Create and apply the clip mask
        mask_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        pygame.draw.polygon(mask_surface, (255, 255, 255, 255), screen_points, 0)
        base_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Copy the result to the main surface
        surface.blit(base_surface, (0, 0))
        
        # Draw outline
        pygame.draw.polygon(surface, (255, 255, 255), screen_points, 1)
        
        # Blit the asteroid surface onto the screen
        screen_pos = (int(self.position.x - surface_size//2),
                     int(self.position.y - surface_size//2))
        screen.blit(surface, screen_pos)

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