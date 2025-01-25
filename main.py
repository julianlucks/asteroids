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

    # Create player instance (automatically added to groups)
    player_position_x = SCREEN_WIDTH / 2
    player_position_y = SCREEN_HEIGHT / 2
    player = Player(player_position_x, player_position_y)
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
        
        # Check collisions between the player and asteroids
        for asteroid in asteroids:
            if player.check_collision(asteroid):
                print("Game over!")
                sys.exit()  # Exit the program
        
        # Check collisions between bullets and asteroids
        for asteroid in asteroids:
            for shot in shots:
                if shot.check_collision(asteroid):  # If bullet hits asteroid
                    asteroid.kill()  # Remove the asteroid
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
