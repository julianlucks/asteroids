from circleshape import CircleShape 
from shot import Shot
from constants import *
import pygame

class Player(CircleShape):
    containers = None  # This will be assigned dynamically in main.py

    def __init__(self, x, y, controls=None):
        # Call the parent class's constructor
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0  # Timer to manage shooting cooldown
        
        # Set control scheme (default to player 1 controls)
        if controls is None:
            self.controls = {
                'left': PLAYER1_LEFT,
                'right': PLAYER1_RIGHT,
                'forward': PLAYER1_FORWARD,
                'backward': PLAYER1_BACKWARD,
                'shoot': PLAYER1_SHOOT
            }
        else:
            self.controls = controls

        # Stun mechanics
        self.stun_timer = 0
        self.is_stunned = False
        self.knockback_velocity = pygame.Vector2(0, 0)

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
        # Update stun status
        if self.is_stunned:
            self.stun_timer -= dt
            if self.stun_timer <= 0:
                self.is_stunned = False
                self.knockback_velocity = pygame.Vector2(0, 0)
            else:
                # Apply knockback and spin while stunned
                self.position += self.knockback_velocity * dt
                self.rotation += PLAYER_STUN_SPIN_SPEED * dt
                return  # Skip normal controls while stunned

        keys = pygame.key.get_pressed()

        # Decrease the shoot timer by dt
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if keys[self.controls['left']]:  # turn left
            self.rotate(dt, -1)  # Pass -1 for left
        if keys[self.controls['right']]:
            self.rotate(dt, 1)  # Pass 1 for right
        if keys[self.controls['forward']]:
            self.move(dt)
        if keys[self.controls['backward']]:
            self.move(dt, -1)  # Move backward
        # Shoot if shoot key is pressed and cooldown has expired
        if keys[self.controls['shoot']] and self.shoot_timer <= 0:
            self.shoot()

    def move(self, dt, direction=1):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * direction
    
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

    def stun(self, asteroid_position):
        """Stun the player and knock them back from the asteroid"""
        self.is_stunned = True
        self.stun_timer = PLAYER_STUN_DURATION
        
        # Calculate knockback direction (away from asteroid)
        knockback_direction = self.position - asteroid_position
        if knockback_direction.length() > 0:  # Avoid division by zero
            knockback_direction = knockback_direction.normalize()
        else:
            knockback_direction = pygame.Vector2(1, 0)  # Default direction if positions are the same
            
        # Set knockback velocity
        self.knockback_velocity = knockback_direction * PLAYER_KNOCKBACK_SPEED