import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion

def main():
    pygame.init()
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Load and scale background image
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set up font for score display
    score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

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
    Explosion.containers = (updatable, drawable)

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

        # Draw background
        screen.blit(background_image, (0, 0))

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
                    # Award points to the shot's owner
                    if shot.owner:
                        shot.owner.add_score(SCORE_POINTS)
                    asteroid.split()  # Remove the asteroid
                    shot.kill()  # Remove the shot

        # Draw all objects in the drawable group
        for obj in drawable:
            obj.draw(screen)

        # Draw scores
        # Player 1 score (left side)
        score_text1 = score_font.render(str(player1.score), True, player1.color)
        screen.blit(score_text1, (SCORE_PADDING, SCORE_PADDING))

        # Player 2 score (right side)
        score_text2 = score_font.render(str(player2.score), True, player2.color)
        score_rect2 = score_text2.get_rect()
        screen.blit(score_text2, (SCREEN_WIDTH - score_rect2.width - SCORE_PADDING, SCORE_PADDING))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate at 60 FPS and get delta time
        framerate = 60
        dt = clock.tick(framerate) / 1000  # Convert milliseconds to seconds

if __name__ == "__main__":
    main()
