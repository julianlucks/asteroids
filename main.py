import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion

class Game:
    def __init__(self):
        pygame.init()
        # Initialize sound system
        if SOUND_ENABLED:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            # Load and configure sounds
            self.sounds = {
                'standard_attack': self._load_sound(SOUND_STANDARD_ATTACK, ATTACK_SOUND_VOLUME),
                'super_attack': self._load_sound(SOUND_SUPER_ATTACK, SUPER_ATTACK_SOUND_VOLUME),
                'big_explosion': self._load_sound(SOUND_BIG_EXPLOSION, EXPLOSION_SOUND_VOLUME),
                'medium_explosion': self._load_sound(SOUND_MEDIUM_EXPLOSION, EXPLOSION_SOUND_VOLUME),
                'small_explosion': self._load_sound(SOUND_SMALL_EXPLOSION, EXPLOSION_SOUND_VOLUME),
                'stunned': self._load_sound(SOUND_STUNNED, STUN_SOUND_VOLUME)
            }
            
            # Initialize music system
            self.current_theme = 1
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.load(MUSIC_THEME_1)
            pygame.mixer.music.play(0)  # Play once, don't loop
            
            # Set up music end event handler
            pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids!")
        self.clock = pygame.time.Clock()

        # Load and scale background image
        self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set up font for score display
        self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

        # Create groups
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

        # Assign groups to the Player class
        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        Shot.containers = (self.shots, self.updatable, self.drawable)
        Explosion.containers = (self.updatable, self.drawable)

        # Pass game instance to classes for sound access
        Shot.game = self
        Asteroid.game = self
        Player.game = self

        # Create players with their initial positions and controls
        player1_x = SCREEN_WIDTH // 4
        player1_y = SCREEN_HEIGHT // 2
        player1_controls = {
            'left': PLAYER1_LEFT,
            'right': PLAYER1_RIGHT,
            'forward': PLAYER1_FORWARD,
            'backward': PLAYER1_BACKWARD,
            'shoot': PLAYER1_SHOOT,
            'super': PLAYER1_SUPER
        }
        self.player1 = Player(player1_x, player1_y, player1_controls, color=(0, 255, 0))  # Green

        player2_x = 3 * SCREEN_WIDTH // 4
        player2_y = SCREEN_HEIGHT // 2
        player2_controls = {
            'left': PLAYER2_LEFT,
            'right': PLAYER2_RIGHT,
            'forward': PLAYER2_FORWARD,
            'backward': PLAYER2_BACKWARD,
            'shoot': PLAYER2_SHOOT,
            'super': PLAYER2_SUPER
        }
        self.player2 = Player(player2_x, player2_y, player2_controls, color=(207, 159, 255))  # Light blue

        # Create an asteroid field instance
        self.asteroid_field = AsteroidField()

        # Initialize delta time variable
        self.dt = 0

    def _load_sound(self, path, volume):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume * SOUND_VOLUME)
            return sound
        except:
            print(f"Warning: Could not load sound file: {path}")
            return None
            
    def get_sound(self, name):
        if SOUND_ENABLED and name in self.sounds:
            return self.sounds[name]
        return None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.USEREVENT + 1:  # Music ended event
                # Switch to the other theme
                self.current_theme = 2 if self.current_theme == 1 else 1
                next_theme = MUSIC_THEME_1 if self.current_theme == 1 else MUSIC_THEME_2
                try:
                    pygame.mixer.music.load(next_theme)
                    pygame.mixer.music.play(0)  # Play once, don't loop
                except pygame.error as e:
                    print(f"Error loading music theme: {e}")
        return True

    def run(self):
        running = True
        # Game Loop
        while running:
            # Event handling
            running = self.handle_events()

            # Draw background
            self.screen.blit(self.background_image, (0, 0))

            # Update all objects in the updatable group
            for obj in self.updatable:
                obj.update(self.dt)
            
            # Check collisions between players and asteroids
            for asteroid in self.asteroids:
                # Check player 1 collision
                if self.player1.check_collision(asteroid):
                    self.player1.stun(asteroid.position)
                # Check player 2 collision
                if self.player2.check_collision(asteroid):
                    self.player2.stun(asteroid.position)
            
            # Check collisions between bullets and asteroids
            for asteroid in self.asteroids:
                for shot in self.shots:
                    if shot.check_collision(asteroid):  # If bullet hits asteroid
                        # Award points to the shot's owner
                        if shot.owner:
                            shot.owner.add_score(SCORE_POINTS)
                        asteroid.split()  # Remove the asteroid
                        shot.kill()  # Remove the shot

            # Draw all objects in the drawable group
            for obj in self.drawable:
                obj.draw(self.screen)

            # Draw scores
            # Player 1 score (left side)
            score_text1 = self.score_font.render(str(self.player1.score), True, self.player1.color)
            self.screen.blit(score_text1, (SCORE_PADDING, SCORE_PADDING))

            # Player 2 score (right side)
            score_text2 = self.score_font.render(str(self.player2.score), True, self.player2.color)
            score_rect2 = score_text2.get_rect()
            self.screen.blit(score_text2, (SCREEN_WIDTH - score_rect2.width - SCORE_PADDING, SCORE_PADDING))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate at 60 FPS and get delta time
            framerate = 60
            self.dt = self.clock.tick(framerate) / 1000  # Convert milliseconds to seconds

if __name__ == "__main__":
    game = Game()
    game.run()
