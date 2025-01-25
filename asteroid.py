from circleshape import CircleShape 
from constants import ASTEROID_MIN_RADIUS
import pygame
import random

class Asteroid(CircleShape):
    containers = None
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt  # Update position using parent class velocity
    
    def split(self):
        # Remove the current asteroid
        self.kill()
        # If the asteroid is too small, it should not split further
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        # Generate a random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)
        # Create two new velocity vectors by rotating the current velocity
        velocity1 = self.velocity.rotate(random_angle) * 1.2  # Rotate and scale up
        velocity2 = self.velocity.rotate(-random_angle) * 1.2  # Rotate and scale up in the opposite direction
        # Compute the radius of the new smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # Create two new asteroids at the same position with the smaller radius
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = velocity1

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = velocity2

        # Add the new asteroids to the appropriate sprite groups
        if Asteroid.containers:
            for group in Asteroid.containers:
                group.add(asteroid1)
                group.add(asteroid2)