import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Asset paths
BACKGROUND_IMAGE_PATH = "pics/background_stars.jpg"

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 2.0  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3
SHOT_RADIUS = 5

# Asteroid appearance
ASTEROID_BASE_COLOR = (70, 70, 70)    # Dark gray base
ASTEROID_CRATER_COLOR = (40, 40, 40)  # Darker gray for craters
ASTEROID_HIGHLIGHT_COLOR = (100, 100, 100)  # Lighter gray for highlights
ASTEROID_CRATER_COUNT = 6  # Number of craters per asteroid
ASTEROID_NOISE_SCALE = 0.15  # Scale of the surface noise (relative to radius)
ASTEROID_MIN_POINTS = 8  # Minimum number of points for lumpy shape
ASTEROID_MAX_POINTS = 12  # Maximum number of points for lumpy shape
ASTEROID_MIN_VARIATION = 0.7  # Minimum radius multiplier for lumpiness
ASTEROID_MAX_VARIATION = 1.3  # Maximum radius multiplier for lumpiness

# Explosion effects
EXPLOSION_PARTICLE_COUNT = 12
EXPLOSION_PARTICLE_SPEED = 200
EXPLOSION_PARTICLE_LIFETIME = 0.7  # seconds
EXPLOSION_PARTICLE_SIZE = 3

# Exhaust effects
EXHAUST_PARTICLE_LIFETIME = 0.5  # seconds
EXHAUST_PARTICLE_SPEED = 150
EXHAUST_PARTICLE_SIZE = 3
EXHAUST_SPAWN_RATE = 0.01  # seconds between particles
EXHAUST_COLOR = (255, 165, 0)  # Brighter orange

# Score display
SCORE_FONT_SIZE = 32
SCORE_PADDING = 20  # Padding from screen edges
SCORE_POINTS = 100  # Points per asteroid hit

# Stun mechanics
PLAYER_STUN_DURATION = 0.7  # seconds
PLAYER_KNOCKBACK_SPEED = 400  # pixels per second
PLAYER_STUN_SPIN_SPEED = 720  # degrees per second

# Player 1 controls (WASD + SPACE)
PLAYER1_LEFT = pygame.K_a
PLAYER1_RIGHT = pygame.K_d
PLAYER1_FORWARD = pygame.K_w
PLAYER1_BACKWARD = pygame.K_s
PLAYER1_SHOOT = pygame.K_SPACE

# Player 2 controls (Arrow keys + Numpad 0)
PLAYER2_LEFT = pygame.K_LEFT
PLAYER2_RIGHT = pygame.K_RIGHT
PLAYER2_FORWARD = pygame.K_UP
PLAYER2_BACKWARD = pygame.K_DOWN
PLAYER2_SHOOT = pygame.K_KP_0
