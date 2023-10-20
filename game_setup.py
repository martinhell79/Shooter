import pygame
import constants as const
import os
import random

# Init game variables
GameState = {
    "Start_Screen": 0,
    "Intro_Screen": 1,
    "Playing": 2,
    "Game_Over": 3,
    "Highscore_Entry": 4,
}
CurrentState = 'Start_Screen'


pygame.init() # Initialize Pygame

pygame.mixer.init() # Initialize sounds
SOUND_DIR = "sound"
SOUND_LASER = pygame.mixer.Sound(os.path.join(SOUND_DIR, '420365__bolkmar__sfx-laser-shot-s-modified.wav'))
SOUND_EXPLOSION = pygame.mixer.Sound(os.path.join(SOUND_DIR, '186958__readeonly__explosion7.wav'))
SOUND_TIME_EXTENSION = pygame.mixer.Sound(os.path.join(SOUND_DIR, '398194__inspectorj__cuckoo-clock-single-a.wav'))

# Handle screen
num_displays = pygame.display.get_num_displays() #Use this to let user choose screen within the game later
chosen_screen = 0  # This could be an index selected by the player
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=chosen_screen) # Create the screen in fullscreen mode
const.screen_width, const.screen_height = screen.get_size() # Retrieve the actual screen dimensions


#Allow holding key down to enable multiple chars
pygame.key.set_repeat(500, 50)

pygame.font.init() # Initialize Font
const.DEFAULT_FONT = pygame.font.SysFont(None, const.screen_width//const.DEFAULT_FONT_SIZE_MODIFIER)

TRANSPARENT = (0, 0, 0, 0)

start_time = 0 #This is re-initialized when game is started

# Keep track of when bonus circles pop up and how much bonus time to add
spawn_time_circles = [8 + random.randint(0, 4), 18 + random.randint(0, 5), 31 + random.randint(0, 1)]
time_bonus = 0
last_time = 0
score = 0
planes = []
objects = []
bonus_circle = []

pygame.display.set_caption('Point and Click Shooting Game') # Window title

#name and email for players
user_name = ''
user_email = ''

def import_animation(vfx_dir):
    vfx_frames = []
    for filename in sorted(os.listdir(vfx_dir)):
        if filename.endswith('.png'):
            frame = pygame.image.load(os.path.join(vfx_dir, filename))
            vfx_frames.append(frame)

    return vfx_frames

# Load all images
try:
    # gameplay
    background_images = [
        pygame.image.load("./img/bg1920x1080.jpg").convert_alpha()
    ]
    background_image = pygame.transform.scale(background_images[0], (const.screen_width, const.screen_height))
    planet1 = pygame.image.load("./img/pink.png").convert_alpha()
    planet1 = pygame.transform.scale(planet1, (planet1.get_width() * 0.2, planet1.get_height() * 0.2))
    planet2 = pygame.image.load("./img/green.png").convert_alpha()
    planet2 = pygame.transform.scale(planet2, (planet2.get_width() * 0.28, planet2.get_height() * 0.28))
    planet3 = pygame.image.load("./img/orange.png").convert_alpha()
    planet3 = pygame.transform.scale(planet3, (planet3.get_width() * 0.15, planet3.get_height() * 0.15))

    # Start screen imgs
    ss_background_image = pygame.image.load("./img/ssbg1920x1080.png").convert_alpha()
    ss_background_image = pygame.transform.scale(ss_background_image, (const.screen_width, const.screen_height))
    clear_img = pygame.image.load("./img/clear.png").convert_alpha()
    clear_img = pygame.transform.scale(clear_img, (clear_img.get_width() * 0.8, clear_img.get_height() * 0.8))
    clear_img_w = clear_img.get_width()
    clear_img_h = clear_img.get_height()
    logo_img = pygame.image.load("./img/Logo.png").convert_alpha()
    logo_img = pygame.transform.scale(logo_img, (logo_img.get_width() * 0.9, logo_img.get_height() * 0.9))
    hs_rect = pygame.image.load("./img/HS_rectangle.png").convert_alpha()
    hs_rect = pygame.transform.scale(hs_rect, (const.screen_width * 0.35, const.screen_height * 0.6))
    hs_trophy = pygame.image.load("./img/trophy.png").convert_alpha()
    hs_trophy = pygame.transform.scale(hs_trophy, (hs_rect.get_width() * 0.2, hs_rect.get_width() * 0.2))
    start_img = pygame.image.load("./img/Start_button.png").convert_alpha()
    start_img = pygame.transform.scale(start_img, (start_img.get_width() * 1, start_img.get_height() * 1))


    # flying objects
    FLYING_OBJECT = pygame.image.load("img/cyber.png") 
    FLYING_OBJECT_WIDTH = int(FLYING_OBJECT.get_width() * const.scale_flying_object)
    FLYING_OBJECT_HEIGHT = int(FLYING_OBJECT.get_height() * const.scale_flying_object)
    FLYING_OBJECT = pygame.transform.scale(FLYING_OBJECT, (FLYING_OBJECT_WIDTH, FLYING_OBJECT_HEIGHT))
    
    #plane flying left
    PLANE_L = pygame.image.load("img/plane_l.png")
    PLANE_L_WIDTH = int(PLANE_L.get_width() * const.scale_plane)
    PLANE_L_HEIGHT = int(PLANE_L.get_height() * const.scale_plane)
    PLANE_L = pygame.transform.scale(PLANE_L, (PLANE_L_WIDTH, PLANE_L_HEIGHT))
    
    #plane flying right
    PLANE_R = pygame.image.load("img/plane_r.png")
    PLANE_R_WIDTH = int(PLANE_R.get_width() * const.scale_plane)
    PLANE_R_HEIGHT = int(PLANE_R.get_height() * const.scale_plane)
    PLANE_R = pygame.transform.scale(PLANE_R, (PLANE_R_WIDTH, PLANE_R_HEIGHT))

    # Clock for bonus time
    BONUS_TIME_CLOCK = pygame.image.load("./img/clock.png").convert_alpha()
    BONUS_TIME_CLOCK_WIDTH = int(BONUS_TIME_CLOCK.get_width() * const.scale_bonus_time_clock)
    BONUS_TIME_CLOCK_HEIGHT = int(BONUS_TIME_CLOCK.get_height() * const.scale_bonus_time_clock)
    BONUS_TIME_CLOCK = pygame.transform.scale(BONUS_TIME_CLOCK, (BONUS_TIME_CLOCK_WIDTH, BONUS_TIME_CLOCK_HEIGHT))

    # End_screen imgs
    hand_img = pygame.image.load("./img/robot-hand.png").convert_alpha()
    hand_img = pygame.transform.scale(hand_img, (hand_img.get_width() * 0.7, hand_img.get_height() * 0.7))
    
    # print mask. Just to check that masking works. Will not be visible when we add background on top of it.
    mask = pygame.mask.from_surface(PLANE_R)
    for x in range(mask.get_size()[0]):
        for y in range(mask.get_size()[1]):
            if mask.get_at((x, y)):
                pygame.draw.rect(screen, const.YELLOW, (x, y, 1, 1))  # Draw a pixel
    
    crosshair_image = pygame.image.load("img/crosshair.png")
    crosshair_image = pygame.transform.scale(crosshair_image, (50, 50))
    # Define the hotspot coordinates (center of the crosshair)
    hotspot = (crosshair_image.get_width() // 2, crosshair_image.get_height() // 2)

    # Import explosion VFX
    VFX_EXPLOSION = import_animation(vfx_dir="img/effects/explosion")

    # Import laser shot VFX
    VFX_LASER = import_animation(vfx_dir="img/effects/laser")
    



except pygame.error:
    print("Error loading the background or flying object image.")

