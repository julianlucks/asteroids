import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def check_collision(self, other_circle):
        # Calculate distance between this circle and another circle
        distance = self.position.distance_to(other_circle.position) 
        # Check if the distance is less than or equal to the sum of their radii
        return distance <= (self.radius + other_circle.radius)

    def wrap_position(self):
        """Wrap the object's position around the screen edges"""
        # Wrap horizontally
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        # Wrap vertically
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius