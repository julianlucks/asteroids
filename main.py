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

    # Create a Clock instance
    clock = pygame.time.Clock()
    # Create player instance
    player_position_x = SCREEN_WIDTH / 2
    player_position_y = SCREEN_HEIGHT / 2
    player = Player(player_position_x, player_position_y)

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
        color = (0,0,0)
        screen.fill(color)
        # draw player
        player.draw(screen)
        # move according to keystrokes
        player.update(dt)
        # Update the display
        pygame.display.flip()
        # Cap the frame rate at 60 FPS and get delta time
        framerate = 60
        dt = clock.tick(framerate) / 1000 # Convert milliseconds to seconds

if __name__ == "__main__":
    main()