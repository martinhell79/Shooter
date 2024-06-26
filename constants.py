# The size of non-flying objects
OBJ_SIZE = 20  

# Shootable images and how to scale them. Adding more array entries will ranomize which image is used in each new spawn.
flying_objects_data = [
    ("img/cyber_l.png", "img/cyber_r.png", 0.9)
]

scale_bonus_time_clock = 0.5

# Set min and max speed of flying objects
MIN_SPEED_FLYING_OBJECT = 100
MAX_SPEED_FLYING_OBJECT = 300

# Scale planes if images are not correct size
scale_plane = 0.6

# Set min and max speed of flying objects
MIN_SPEED_PLANE = 250
MAX_SPEED_PLANE = 400

# Set radius for bonus time circles
BONUS_CIRCLE_RADIUS = 30

BONUS_TIME = 3 # seconds

# penalty for hitting a plane
PLANE_PENALTY = -500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

TRANSPARENT = (0, 0, 0, 0)

DEFAULT_FONT = None
DEFAULT_FONT_SIZE_MODIFIER = 30

#Will be initialized upon setup
screen_width = 0
screen_height = 0

# Max plays per email
MAX_PLAYS_PER_EMAIL = 5

# Allowed characters
ALLOWED_CHARS = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    "!#$%&'*+-/=?^_`{|}~.@"
)