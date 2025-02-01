from circleshape import CircleShape 
from shot import Shot
from constants import *
from exhaust import ExhaustSystem
from explosion import Explosion
import pygame
import math

class Player(CircleShape):
    containers = None
    game = None  # Will hold reference to game instance for sound access

    def __init__(self, x, y, controls=None, color="white"):
        # Call the parent class's constructor
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0  # Timer for normal shooting cooldown
        self.super_timer = 0  # Start with super attack ready
        self.color = color  # Store player color
        self.score = 0  # Initialize score
        
        # Physics properties
        self.velocity = pygame.Vector2(0, 0)  # Current velocity vector
        
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
                'shoot': PLAYER1_SHOOT,
                'super': PLAYER1_SUPER
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

    # function to define the player rocket shape
    def triangle(self):
        # Calculate base vectors
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
        
        # Calculate key points
        # Nose of the rocket (front point)
        nose = self.position + forward * self.radius
        
        # Base points (wider than before)
        base_width = self.radius * 0.8  # Slightly narrower than before
        base_right = self.position - forward * (self.radius * 0.8) + right * base_width
        base_left = self.position - forward * (self.radius * 0.8) - right * base_width
        
        # Engine nozzle points (creates a small indent for the engine)
        nozzle_width = base_width * 0.4  # Engine is 40% of base width
        nozzle_back = self.radius * 0.9  # Slightly forward of the base
        nozzle_right = self.position - forward * nozzle_back + right * nozzle_width
        nozzle_left = self.position - forward * nozzle_back - right * nozzle_width
        
        # Return points in drawing order
        return [
            nose,           # Front point
            base_right,     # Right wing
            nozzle_right,   # Right engine point
            nozzle_left,    # Left engine point
            base_left,      # Left wing
        ]

    # function to draw the player rocket
    def draw(self, screen):
        # Draw exhaust first so it appears behind the ship
        self.exhaust.draw(screen)

        # Get the points for the rocket shape
        points = self.triangle()
        
        # Convert string color names to RGB tuples if needed
        if isinstance(self.color, str):
            try:
                base_color = pygame.Color(self.color)
                base_color = (base_color.r, base_color.g, base_color.b)
            except ValueError:
                base_color = (255, 255, 255)  # Default to white if invalid color name
        else:
            base_color = self.color
        
        # Determine colors based on stun state
        if self.is_stunned:
            # Flash between normal color and a dimmer version during stun
            if int(self.stun_timer * 10) % 2:
                fill_color = tuple(int(c * 0.3) for c in base_color)  # More dimmed when stunned
                outline_color = tuple(int(c * 0.5) for c in base_color)
            else:
                # Normal colors when not in flash frame
                fill_color = tuple(int(c * 0.7) for c in base_color)
                outline_color = base_color
        else:
            # Normal colors when not stunned
            fill_color = tuple(int(c * 0.7) for c in base_color)
            outline_color = base_color
        
        # Draw filled rocket
        pygame.draw.polygon(screen, fill_color, points, 0)
        
        # Draw outline
        pygame.draw.polygon(screen, outline_color, points, 2)
        
        # Only draw detail line when not stunned
        if not self.is_stunned:
            # Add a small line detail near the nose for style
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
            detail_back = self.radius * 0.3  # Position of detail line
            detail_width = self.radius * 0.4  # Width of detail line
            detail_start = self.position + forward * (self.radius - detail_back) - right * detail_width
            detail_end = self.position + forward * (self.radius - detail_back) + right * detail_width
            pygame.draw.line(screen, outline_color, detail_start, detail_end, 1)

    # function to rotate the player rocket
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
                self.velocity = pygame.Vector2(0, 0)  # Reset velocity after stun
            else:
                # Apply knockback during stun
                self.position += self.knockback_velocity * dt
                self.rotation += PLAYER_STUN_SPIN_SPEED * dt
                self.wrap_position()
                # Update exhaust but mark as not moving while stunned
                self.exhaust.update(dt, self.position.x, self.position.y, 
                                  self.rotation, False, 0)
                return

        # Reset movement flags
        self.is_moving = False
        self.move_direction = 1
        
        # Get current keyboard state
        keys = pygame.key.get_pressed()

        # Handle rotation (independent of movement)
        if keys[self.controls['left']]:
            self.rotate(dt, -1)
        if keys[self.controls['right']]:
            self.rotate(dt, 1)

        # Handle movement
        if keys[self.controls['forward']]:
            self.is_moving = True
            self.move_direction = 1
            self.move(dt)
        if keys[self.controls['backward']]:
            self.is_moving = True
            self.move_direction = -1
            self.move(dt, -1)

        # Apply drag to slow down
        if self.velocity.length() > 0:
            drag = self.velocity * DRAG_FACTOR
            self.velocity -= drag * dt

        # Update position based on velocity
        self.position += self.velocity * dt
        self.wrap_position()

        # Update timers
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
        if self.super_timer > 0:
            self.super_timer -= dt

        # Handle shooting
        if keys[self.controls['shoot']] and self.shoot_timer <= 0:
            self.shoot()
            
        # Handle super attack
        if keys[self.controls['super']] and self.super_timer <= 0:
            self.super_attack()
            
        # Update exhaust system - use velocity for intensity
        speed = self.velocity.length() / MAX_SPEED  # Normalize speed to 0-1
        # Determine if we're braking
        is_braking = keys[self.controls['backward']] and self.velocity.length() > 0
        if is_braking:
            # Show exhaust in opposite direction when braking
            brake_rotation = (self.rotation + 180) % 360
            self.exhaust.update(dt, self.position.x, self.position.y, brake_rotation,
                              True, speed)
        else:
            # Normal exhaust
            self.exhaust.update(dt, self.position.x, self.position.y, self.rotation,
                              self.is_moving, speed)

    def super_attack(self):
        # Only allow super attack if cooldown is done
        if self.super_timer <= 0:
            # Reset the super attack timer
            self.super_timer = SUPER_ATTACK_COOLDOWN
            
            # Create a circular wave of bullets
            for i in range(SUPER_ATTACK_BULLETS):
                # Calculate angle for each bullet
                angle = 360 / SUPER_ATTACK_BULLETS * i
                # Create velocity vector for this angle
                shot_velocity = pygame.Vector2(0, 1).rotate(angle) * SUPER_ATTACK_SPEED
                
                # Create the shot with a different color for super attacks
                shot = Shot(self.position.x, self.position.y, shot_velocity, owner=self)
                
                # Add the shot to the appropriate groups
                if Shot.containers:
                    for group in Shot.containers:
                        group.add(shot)
            
            # Play super attack sound if available
            if hasattr(Shot, 'game') and Shot.game:
                sound = Shot.game.get_sound('super_attack')
                if sound:
                    sound.play()
            
            # Create a visual effect for the super attack
            flash = Explosion(self.position.x, self.position.y, self.color)
        else:
            print(f"Super attack on cooldown: {self.super_timer:.1f} seconds")  # Debug print

    def move(self, dt, direction=1):
        # Calculate thrust direction based on ship's rotation
        thrust_dir = pygame.Vector2(0, 1).rotate(self.rotation)
        
        if direction < 0:
            # For backward key, first act as brake
            current_speed = self.velocity.length()
            if current_speed > 10:  # Only brake if moving significantly
                # Get current movement direction
                move_dir = self.velocity.normalize()
                # Calculate angle between movement and facing direction
                angle = thrust_dir.angle_to(move_dir)
                # If moving roughly forward, apply braking force
                if abs(angle) < 90:
                    # Apply brake force against current velocity
                    brake_force = self.velocity.normalize() * THRUST_FORCE * 1.5 * dt
                    self.velocity -= brake_force
                    # Prevent jitter by setting very small velocities to zero
                    if self.velocity.length() < 10:
                        self.velocity = pygame.Vector2(0, 0)
                    return
            
            # Apply backward thrust if nearly stopped or moving backward
            thrust = -thrust_dir * THRUST_FORCE * dt * BACKWARD_MULTIPLIER
        else:
            # Normal forward thrust
            thrust = thrust_dir * THRUST_FORCE * dt
        
        # Add thrust to current velocity
        self.velocity += thrust
        
        # Limit speed
        speed = self.velocity.length()
        if speed > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)

    def shoot(self):
        # Reset the shoot timer to the cooldown duration
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        
        # Calculate bullet velocity based on ship's rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot_velocity = forward * PLAYER_SHOOT_SPEED
        
        # Create the shot
        shot = Shot(self.position.x, self.position.y, shot_velocity, owner=self)
        
        # Play shooting sound if available
        if hasattr(Shot, 'game') and Shot.game:
            sound = Shot.game.get_sound('standard_attack')
            if sound:
                sound.play()
                
    def stun(self, asteroid_pos):
        if not self.is_stunned:
            self.is_stunned = True
            self.stun_timer = PLAYER_STUN_DURATION
            
            # Calculate knockback direction from asteroid
            knockback_dir = self.position - pygame.Vector2(asteroid_pos)
            if knockback_dir.length() > 0:
                knockback_dir.normalize_ip()
                # Add current velocity to knockback
                self.knockback_velocity = knockback_dir * MAX_SPEED + self.velocity * 0.5
            
            # Play stun sound if available
            if hasattr(Player, 'game') and Player.game:
                sound = Player.game.get_sound('stunned')
                if sound:
                    sound.play()

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