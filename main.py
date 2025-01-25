import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Assign groups to the Player class
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    # Create player instances (automatically added to groups)
    player1_x = SCREEN_WIDTH / 3
    player1_y = SCREEN_HEIGHT / 2
    player1 = Player(player1_x, player1_y, color=(144, 238, 144))  # Light green

    player2_x = (SCREEN_WIDTH / 3) * 2
    player2_y = SCREEN_HEIGHT / 2
    player2_controls = {
        'left': PLAYER2_LEFT,
        'right': PLAYER2_RIGHT,
        'forward': PLAYER2_FORWARD,
        'backward': PLAYER2_BACKWARD,
        'shoot': PLAYER2_SHOOT
    }
    player2 = Player(player2_x, player2_y, player2_controls, color=(207, 159, 255))  # Light blue

    # Create an asteroid field instance
    asteroid_field = AsteroidField()

    # Create a Clock instance
    clock = pygame.time.Clock()

    # Initialize delta time variable
    dt = 0

    running = True
    # Game Loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Fill the screen with black
        color = (0, 0, 0)
        screen.fill(color)

        # Update all objects in the updatable group
        for obj in updatable:
            obj.update(dt)
        
        # Check collisions between players and asteroids
        for asteroid in asteroids:
            # Check player 1 collision
            if player1.check_collision(asteroid):
                player1.stun(asteroid.position)
            # Check player 2 collision
            if player2.check_collision(asteroid):
                player2.stun(asteroid.position)
        
        # Check collisions between bullets and asteroids
        for asteroid in asteroids:
            for shot in shots:
                if shot.check_collision(asteroid):  # If bullet hits asteroid
                    asteroid.split()  # Remove the asteroid
                    shot.kill()  # Remove the shot

        # Draw all objects in the drawable group
        for obj in drawable:
            obj.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate at 60 FPS and get delta time
        framerate = 60
        dt = clock.tick(framerate) / 1000  # Convert milliseconds to seconds

if __name__ == "__main__":
    main()
