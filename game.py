import pygame
import random
import time
import highscores as hs
import math
from math import radians, cos, sin

#Init constants
OBJ_SIZE = 40
TIME_LIMIT = 60
scale_flying_object = 0.5
min_speed = 10
max_speed = 20

GameState = {
    "Playing": 0,
    "Game Over": 1,
    "Highscore Entry": 2,
}
# Initialize Pygame
pygame.init()

# Create the screen in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Retrieve the actual screen dimensions
width, height = screen.get_size()

# Initialize Font
pygame.font.init()
font = pygame.font.SysFont(None, 36)  # Default font, size 36

# Add a list to store individual score pop-ups
score_popups = []

remaining_time = TIME_LIMIT  # 30 seconds
#game_over = False
start_time = pygame.time.get_ticks()

# Window title
pygame.display.set_caption('Point and Click Shooting Game')

# define background
try:
    background_image = pygame.image.load("back.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (width, height))
    flying_object = pygame.image.load("cyber.png") 
    # Calculate the new width and height based on the percentage scale
    new_width = int(flying_object.get_width() * scale_flying_object)
    new_height = int(flying_object.get_height() * scale_flying_object)
    # Resize the image to the calculated dimensions
    flying_object = pygame.transform.scale(flying_object, (new_width, new_height))
    sprite_mask = pygame.mask.from_surface(flying_object)
    # print mask
    for x in range(sprite_mask.get_size()[0]):
        for y in range(sprite_mask.get_size()[1]):
            if sprite_mask.get_at((x, y)):
                pygame.draw.rect(screen, (255, 255, 255), (x, y, 1, 1))  # Draw a red pixel
except pygame.error:
    print("Error loading the background or flying object image.")

'''
#function to update background image
def change_background(score):
    if score < 1000:
        return background_images[0]
    elif score < 2000:
        return background_images[0]
    else:
        return background_images[0]
'''

def popup_hitscore(score, x, y):
    # Create a text surface with a transparent background
    font = pygame.font.Font(None, 48)
    text = font.render(str(score), True, (255, 255, 255), (0, 0, 0, 0))  # (0, 0, 0, 0) is transparent

    # Get the text rect to position it
    text_rect = text.get_rect()
    text_rect.center = (x+10, y+10)

    # Blit the text surface onto the game screen
    screen.blit(text, text_rect)

def is_click_on_sprite(mouse_x, mouse_y, sprite_x, sprite_y, sprite_mask):
    # Calculate the local coordinates within the sprite
    local_x, local_y = mouse_x - sprite_x, mouse_y - sprite_y
    print(mouse_x, mouse_y, sprite_x, sprite_y)
    # Check if the local coordinates are within the sprite's dimensions
    if 0 <= local_x < sprite_mask.get_size()[0] and 0 <= local_y < sprite_mask.get_size()[1]:
        # Check if the corresponding pixel in the mask is set (collision)
        if sprite_mask.get_at((local_x, local_y)):
            return True

    return False


# Object Class
class FlyingObject:
    def __init__(self, x, y, image, color, velocity, speed):
        self.x = x
        self.y = y
        #self.radius = radius
        self.color = color
        self.velocity = velocity
        self.timestamp = time.time()  # Record the time when the object is spawned
        self.start_score = 100 + (speed - min_speed) * (100 / (max_speed - min_speed))  # Affine function based on speed
        self.end_score = 20 + (speed - min_speed) * (20 / (max_speed - min_speed))  # Affine function based on speed
        self.image = image

        # Calculate intersection point with each edge of the screen
        t_to_left = (0 - x) / velocity[0] if velocity[0] < 0 else float('inf')
        t_to_right = (width - x) / velocity[0] if velocity[0] > 0 else float('inf')
        t_to_top = (0 - y) / velocity[1] if velocity[1] < 0 else float('inf')
        t_to_bottom = (height - y) / velocity[1] if velocity[1] > 0 else float('inf')

        # Choose the smallest positive t (time to edge)
        t_to_edge = min(t for t in [t_to_left, t_to_right, t_to_top, t_to_bottom] if t > 0)

        # Calculate total_time based on the exact distance to the edge
        self.total_time = t_to_edge

        print(f"Total Time: {self.total_time}")  # Debug print

    def draw(self, screen, font, current_time):
        #see how long the object has been on the screen
        time_elapsed = current_time - self.timestamp  # Should be increasing as time goes on
        
        # Draw circle in new position
        # pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        screen.blit(self.image, (int(self.x), int(self.y)))
        #Compute and display current score for object
        current_score = self.end_score + (self.start_score - self.end_score) * (1 - (time_elapsed / self.total_time))
        score_text = font.render(f"{int(current_score)}", True, (255, 255, 255))
        screen.blit(score_text, (int(self.x) - 25, int(self.y)))
        
        
    
    def move(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

def spawn_object():
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    angle_range = {
        'top': (260, 280),
        'bottom': (80, 100),
        'left': (350, 370),
        'right': (170, 190)
    }
    min_angle, max_angle = angle_range[edge]

    if edge in ['top', 'bottom']:
        initial_x = random.randint(int(0.15 * width), int(0.85 * width))
        initial_y = -50 if edge == 'top' else height + 50
    else:
        initial_x = -50 if edge == 'left' else width + 50
        initial_y = random.randint(int(0.15 * height), int(0.85 * height))

    angle = radians(random.uniform(min_angle, max_angle))
    speed = random.uniform(min_speed, max_speed)
    
    # Scale the velocity by 100 for more reasonable movement speeds
    velocity = [speed * cos(angle) * 1, -speed * sin(angle) * 1]
    
    return FlyingObject(initial_x, initial_y, flying_object, object_color, velocity, speed)

# Object attributes
#object_radius = OBJ_SIZE
object_color = (255, 0, 0)  # Red



# Initialize the first object and object list
objects = [spawn_object() for _ in range(4)]

# Timer to control the spawning of new objects
next_spawn_time = time.time() + random.uniform(0.1, 0.7)

# Initialize score
score = 0

last_time = time.time()

# Main game loop
currentstate = GameState['Playing'];
running = True
while running:
    if (currentstate == GameState['Playing']):
        screen.fill((255, 255, 255))
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        c_time = pygame.time.get_ticks()
        elapsed_time = (c_time - start_time) // 1000  # Convert milliseconds to seconds
        remaining_time = max(0, TIME_LIMIT - elapsed_time)  # Ensure remaining_time doesn't go below 0
        
        # Draw the background image
        #background_image = change_background(score)
        
        screen.blit(background_image, (0, 0))

        if remaining_time == 0:
            currentstate = GameState['Game Over'];
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for obj in objects[:]:
                    #flying_object_pixels = pygame.PixelArray(obj.image)
                    if is_click_on_sprite(mouse_x, mouse_y, int(obj.x), int(obj.y), sprite_mask):
                    #distance = ((mouse_x - obj.x)**2 + (mouse_y - obj.y)**2)**0.5
                    #if distance <= object_radius:
                        time_elapsed = current_time - obj.timestamp
                        score_increment = int(obj.end_score + (obj.start_score - obj.end_score) * ((obj.total_time - time_elapsed) / obj.total_time))
                        score += score_increment

                        objects.remove(obj)
                        # Add score popup to array
                        score_popups.append({"score": score_increment, "x": mouse_x, "y": mouse_y, "timestamp": current_time})
                    #flying_object_pixels.close()
        
        
        # Move and draw the objects
        for obj in objects:
            obj.move(dt)
            obj.draw(screen, font, current_time)  # Pass the font and current time

        score_text = font.render(f"Score: {int(score)}", True, (0, 0, 0))  # RGB color for white
        screen.blit(score_text, (10, 10))  # Display the text at (10, 10)
        #update timer
        timer_text = font.render(f"Time: {remaining_time}", True, (0, 0, 0))
        screen.blit(timer_text, (width-100, 10))  # Display the timer at (10, 10) on the screen
        
        # Render individual score popups after a hit
        for popup in score_popups[:]:
            elapsed_time = current_time - popup["timestamp"]
            if elapsed_time > 1:  # Display popup for 1 second
                score_popups.remove(popup)
                continue
            popup_hitscore(int(popup['score']), popup['x'], popup['y'])
            
        # Remove objects that have left the screen
        objects = [obj for obj in objects if obj.x >= -50 and obj.x <= width + 50 and obj.y >= -50 and obj.y <= height + 50]

        # Spawn a new object if fewer than 3 are present
        if len(objects) < 4 and current_time >= next_spawn_time:
            objects.append(spawn_object())
            next_spawn_time = current_time + random.uniform(0.1, 0.7)
        pygame.display.flip()  # Update the display

    elif (currentstate == GameState['Game Over']):
        hs.load_highscores()
        hs.update_highscores(score)
        currentstate = GameState['Highscore Entry']

    elif (currentstate == GameState['Highscore Entry']):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill((0, 0, 0))  # Clear the screen
        final_score_text = font.render(f"Final Score: {int(score)}", True, (255, 255, 255))
        screen.blit(final_score_text, (width // 6 , height // 2 - 50))
        hs.display_highscores(pygame, screen, width, height)
        pygame.display.flip()  # Update the display
    

# Print final score (You can also display this on the screen later)
print(f"Final Score: {score}")

# Quit Pygame
pygame.quit()
