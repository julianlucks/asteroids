import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Asset paths
BACKGROUND_IMAGE_PATH = "pics/background_stars.jpg"

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 2.0  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# Player movement
PLAYER_TURN_SPEED = 360  # Degrees per second
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 400
PLAYER_SHOOT_COOLDOWN = 0.25
PLAYER_RADIUS = 15
SHOT_RADIUS = 3  # Size of the projectiles

# Physics constants
THRUST_FORCE = 250      # Reduced acceleration for more subtle movement
MAX_SPEED = 250         # Lower max speed
DRAG_FACTOR = 0.3       # Slightly more drag for better control
BACKWARD_MULTIPLIER = 0.4  # Even weaker backward thrust

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

# Asteroid lighting
LIGHT_DIRECTION = pygame.Vector2(1, -1)  # Light coming from top-right
LIGHT_INTENSITY = 0.7  # Base light intensity
AMBIENT_LIGHT = 0.3   # Minimum light level
CRATER_DEPTH = 0.4    # How "deep" craters appear
BUMP_HEIGHT = 0.2     # How "high" surface bumps appear

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

# Stun settings
PLAYER_STUN_DURATION = 1.0
PLAYER_STUN_SPIN_SPEED = 360  # Degrees per second
PLAYER_KNOCKBACK_SPEED = MAX_SPEED * 1.2  # Slightly faster than max speed

# Player 1 controls (WASD + SPACE)
PLAYER1_LEFT = pygame.K_a
PLAYER1_RIGHT = pygame.K_d
PLAYER1_FORWARD = pygame.K_w
PLAYER1_BACKWARD = pygame.K_s
PLAYER1_SHOOT = pygame.K_SPACE
PLAYER1_SUPER = pygame.K_LALT  # Left Alt for super attack

# Player 2 controls (Arrows + Numpad 0)
PLAYER2_LEFT = pygame.K_LEFT
PLAYER2_RIGHT = pygame.K_RIGHT
PLAYER2_FORWARD = pygame.K_UP
PLAYER2_BACKWARD = pygame.K_DOWN
PLAYER2_SHOOT = pygame.K_KP0  # Numpad 0
PLAYER2_SUPER = pygame.K_KP1  # Numpad 1

# Super attack settings
SUPER_ATTACK_COOLDOWN = 10.0  # Cooldown in seconds
SUPER_ATTACK_BULLETS = 64     # number of bullets
SUPER_ATTACK_SPEED = 350      # Slightly increased speed
