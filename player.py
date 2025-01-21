from circleshape import CircleShape 
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED
import pygame

class Player(CircleShape):
    def __init__(self, x, y):
        # Call the parent class's constructor
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
    # function to define the player stripe shape
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    # function to draw the player stripe
    def draw(self, screen):
        line_color = "white"
        line_width = 2
        points = self.triangle()
        pygame.draw.polygon(screen, line_color, points, line_width)
    # function to rotate the player stripe
    def rotate(self, dt, direction):
        # rotate based on direction (-1 for left, 1 for right)
        self.rotation += direction * PLAYER_TURN_SPEED * dt
    # function for the rotation key bindings
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: # turn left
            self.rotate(dt, -1) # Pass -1 for left
        if keys[pygame.K_d]:
            self.rotate(dt, 1) # Pass 1 for right