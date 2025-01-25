from circleshape import CircleShape 
from constants import SHOT_RADIUS
import pygame

class Shot(CircleShape):
    containers = None  # This will be assigned dynamically in main.py
    
    def __init__(self, x, y, velocity, owner=None):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = velocity
        self.owner = owner  # Store reference to the player who fired this shot

    def update(self, dt):
        # Move the shot according to its velocity
        self.position += self.velocity * dt
        self.wrap_position()  # Wrap position after movement

        # Remove the shot if it goes off-screen
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if not (0 <= self.position.x <= screen_width and 0 <= self.position.y <= screen_height):
            self.kill()  # Remove the shot from all sprite groups

    def draw(self, screen):
        # Draw the shot in the owner's color if available, otherwise white
        color = self.owner.color if self.owner else (255, 255, 255)
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), self.radius)
