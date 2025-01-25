from circleshape import CircleShape 
from constants import ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
import random
import math

class Asteroid(CircleShape):
    containers = None
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Generate random points for lumpy appearance
        self.num_points = random.randint(8, 12)  # Number of points in the polygon
        self.variations = []
        for _ in range(self.num_points):
            # Variation between 0.7 and 1.3 of the radius
            self.variations.append(random.uniform(0.7, 1.3))
        self.rotation = random.uniform(0, 360)  # Random initial rotation
        self.spin_speed = random.uniform(-45, 45)  # Degrees per second

    def get_points(self):
        """Get the current points of the lumpy asteroid"""
        points = []
        for i in range(self.num_points):
            angle = math.radians(360 / self.num_points * i + self.rotation)
            # Calculate point position with variation
            distance = self.radius * self.variations[i]
            x = self.position.x + math.cos(angle) * distance
            y = self.position.y + math.sin(angle) * distance
            points.append((int(x), int(y)))
        return points

    def draw(self, screen):
        points = self.get_points()
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()  # Wrap position after movement
        # Update rotation
        self.rotation += self.spin_speed * dt

    def wrap_position(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

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