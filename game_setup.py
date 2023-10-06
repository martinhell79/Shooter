import pygame
import constants as const


# Init game variables
GameState = {
    "Playing": 0,
    "Game Over": 1,
    "Highscore Entry": 2,
}

pygame.init() # Initialize Pygame
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Create the screen in fullscreen mode
const.screen_width, const.screen_height = screen.get_size() # Retrieve the actual screen dimensions
pygame.font.init() # Initialize Font
const.DEFAULT_FONT = pygame.font.SysFont(None, const.screen_width//50)  # Scale font size to screen size. (Avoid tiny text on 4k)

TRANSPARENT = (0, 0, 0, 0)

remaining_time = const.TIME_LIMIT  # 30 seconds
start_time = pygame.time.get_ticks()

pygame.display.set_caption('Point and Click Shooting Game') # Window title

# Load all images
try:
    background_images = [
        pygame.image.load("./img/bg1920x1080.jpg").convert_alpha()
    ]
    background_image = pygame.transform.scale(background_images[0], (const.screen_width, const.screen_height))
    
    # flying objects
    FLYING_OBJECT = pygame.image.load("img/cyber.png") 
    new_width = int(FLYING_OBJECT.get_width() * const.scale_flying_object)
    new_height = int(FLYING_OBJECT.get_height() * const.scale_flying_object)
    FLYING_OBJECT = pygame.transform.scale(FLYING_OBJECT, (new_width, new_height))
    sprite_mask = pygame.mask.from_surface(FLYING_OBJECT)
    
    #plane
    PLANE = pygame.image.load("img/plane.png")
    new_width = int(PLANE.get_width() * const.scale_plane)
    new_height = int(PLANE.get_height() * const.scale_plane)
    PLANE = pygame.transform.scale(PLANE, (new_width, new_height))
    plane_mask = pygame.mask.from_surface(PLANE)
    # print mask. Just to check that masking works. Will not be visible when we add background on top of it.
    for x in range(sprite_mask.get_size()[0]):
        for y in range(sprite_mask.get_size()[1]):
            if sprite_mask.get_at((x, y)):
                pygame.draw.rect(screen, const.WHITE, (x, y, 1, 1))  # Draw a pixel
    crosshair_image = pygame.image.load("img/crosshair.png")
    crosshair_image = pygame.transform.scale(crosshair_image, (50, 50))
    # Define the hotspot coordinates (center of the crosshair)
    hotspot = (crosshair_image.get_width() // 2, crosshair_image.get_height() // 2)


except pygame.error:
    print("Error loading the background or flying object image.")