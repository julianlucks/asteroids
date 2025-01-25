from circleshape import CircleShape 
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
import pygame

class Player(CircleShape):
    containers = None  # This will be assigned dynamically in main.py

    def __init__(self, x, y):
        # Call the parent class's constructor
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0  # Timer to manage shooting cooldown

        # Add this instance to the assigned groups
        if Player.containers:
            for group in Player.containers:
                group.add(self)

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

    # update the player
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Decrease the shoot timer by dt
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if keys[pygame.K_a]:  # turn left
            self.rotate(dt, -1)  # Pass -1 for left
        if keys[pygame.K_d]:
            self.rotate(dt, 1)  # Pass 1 for right
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt)
        # Shoot if spacebar is pressed and cooldown has expired
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        # Reset the shoot timer to the cooldown duration
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        # Create a shot object at the player's position
        shot_velocity = pygame.Vector2(0, 1)  # Initial direction (upwards)
        shot_velocity = shot_velocity.rotate(self.rotation)  # Rotate to player's direction
        shot_velocity *= PLAYER_SHOOT_SPEED  # Scale to shoot speed

        shot = Shot(self.position.x, self.position.y, shot_velocity)

        # Add the shot to the appropriate groups
        if Shot.containers:
            for group in Shot.containers:
                group.add(shot)