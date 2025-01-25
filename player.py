from circleshape import CircleShape 
from shot import Shot
from constants import *
from exhaust import ExhaustSystem
import pygame

class Player(CircleShape):
    containers = None  # This will be assigned dynamically in main.py

    def __init__(self, x, y, controls=None, color="white"):
        # Call the parent class's constructor
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0  # Timer to manage shooting cooldown
        self.color = color  # Store player color
        self.score = 0  # Initialize score
        
        # Exhaust system
        self.exhaust = ExhaustSystem()
        self.is_moving = False
        self.move_direction = 1  # 1 for forward, -1 for backward

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
        # Draw exhaust first so it appears behind the ship
        self.exhaust.draw(screen)
        
        line_width = 2
        points = self.triangle()
        # Fill the triangle with a slightly darker version of the player's color
        if isinstance(self.color, str):
            fill_color = self.color
        else:
            # Darken the RGB color by multiplying each component by 0.7
            fill_color = tuple(int(c * 0.7) for c in self.color)
        # Draw filled triangle
        pygame.draw.polygon(screen, fill_color, points, 0)
        # Draw outline
        pygame.draw.polygon(screen, self.color, points, line_width)

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
                self.wrap_position()  # Wrap position after movement
                # Update exhaust but mark as not moving while stunned
                self.exhaust.update(dt, self.position.x, self.position.y, 
                                  self.rotation, False, 0)
                return  # Skip normal controls while stunned

        self.is_moving = False  # Reset movement flag
        self.move_direction = 1  # Reset move direction
        keys = pygame.key.get_pressed()

        # Decrease the shoot timer by dt
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if keys[self.controls['left']]:  # turn left
            self.rotate(dt, -1)  # Pass -1 for left
        if keys[self.controls['right']]:
            self.rotate(dt, 1)  # Pass 1 for right
        if keys[self.controls['forward']]:
            self.is_moving = True
            self.move_direction = 1
            self.move(dt)
        if keys[self.controls['backward']]:
            self.is_moving = True
            self.move_direction = -1
            self.move(dt, -1)  # Move backward
        # Shoot if shoot key is pressed and cooldown has expired
        if keys[self.controls['shoot']] and self.shoot_timer <= 0:
            self.shoot()
            
        # Update exhaust system
        self.exhaust.update(dt, self.position.x, self.position.y, self.rotation, 
                          self.is_moving, abs(self.move_direction))

    def move(self, dt, direction=1):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * direction
        self.wrap_position()  # Wrap position after movement
    
    def shoot(self):
        # Reset the shoot timer to the cooldown duration
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        # Create a shot object at the player's position
        shot_velocity = pygame.Vector2(0, 1)  # Initial direction (upwards)
        shot_velocity = shot_velocity.rotate(self.rotation)  # Rotate to player's direction
        shot_velocity *= PLAYER_SHOOT_SPEED  # Scale to shoot speed

        shot = Shot(self.position.x, self.position.y, shot_velocity, owner=self)

        # Add the shot to the appropriate groups
        if Shot.containers:
            for group in Shot.containers:
                group.add(shot)

    def stun(self, asteroid_pos):
        if not self.is_stunned:
            self.is_stunned = True
            self.stun_timer = PLAYER_STUN_DURATION
            
            # Calculate knockback direction (away from asteroid)
            knockback_dir = self.position - asteroid_pos
            knockback_dir = knockback_dir.normalize()
            self.knockback_velocity = knockback_dir * PLAYER_KNOCKBACK_SPEED
            
            # Trigger quick fade for exhaust particles
            self.exhaust.trigger_quick_fade()

    def wrap_position(self):
        # Wrap position around the screen edges
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def add_score(self, points):
        """Add points to the player's score"""
        self.score += points