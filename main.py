import pygame
from constants import *
from player import Player

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

    # Assign groups to the Player class
    Player.containers = (updatable, drawable)

    # Create player instance (automatically added to groups)
    player_position_x = SCREEN_WIDTH / 2
    player_position_y = SCREEN_HEIGHT / 2
    player = Player(player_position_x, player_position_y)

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
