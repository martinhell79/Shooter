import pygame
import random
import time
import constants as const
import highscores as hs
from game_object import FlyingObject
from math import radians, cos, sin
import game_setup


# Init game variables
GAME_STATE = game_setup.GameState

# pygame.init() # Initialize Pygame
screen = game_setup.screen

remaining_time = const.TIME_LIMIT  # 30 seconds
start_time = game_setup.start_time


# Import images

background_image = game_setup.background_image
flying_object = game_setup.FLYING_OBJECT
sprite_mask = game_setup.sprite_mask
crosshair_image = game_setup.crosshair_image
hotspot = game_setup.hotspot

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
    text = font.render(str(score), True, const.YELLOW, const.TRANSPARENT)

    # Get the text rect to position it
    text_rect = text.get_rect()
    text_rect.center = (x+10, y+10)

    # Blit the text surface onto the game screen
    screen.blit(text, text_rect)

def is_click_on_sprite(mouse_x, mouse_y, sprite_x, sprite_y, sprite_mask):
    # Calculate the local coordinates within the sprite
    local_x, local_y = mouse_x - sprite_x, mouse_y - sprite_y
    # print(mouse_x, mouse_y, sprite_x, sprite_y)
    # Check if the local coordinates are within the sprite's dimensions
    if 0 <= local_x < sprite_mask.get_size()[0] and 0 <= local_y < sprite_mask.get_size()[1]:
        # Check if the corresponding pixel in the mask is set (collision)
        if sprite_mask.get_at((local_x, local_y)):
            return True

    return False

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
        initial_x = random.randint(int(0.15 * const.screen_width), int(0.85 * const.screen_width))
        initial_y = -50 if edge == 'top' else const.screen_height + 50
    else:
        initial_x = -50 if edge == 'left' else const.screen_width + 50
        initial_y = random.randint(int(0.15 * const.screen_height), int(0.85 * const.screen_height))

    angle = radians(random.uniform(min_angle, max_angle))
    speed = random.uniform(const.MIN_SPEED_FLYING_OBJECT, const.MAX_SPEED_FLYING_OBJECT)
    
    velocity = [speed * cos(angle), -speed * sin(angle)]
    
    return FlyingObject(initial_x, initial_y, flying_object, velocity, speed)



def start_game():
    #Gameplay variables
    objects = [spawn_object() for _ in range(4)] # Initialize the first object and object list
    next_spawn_time = time.time() + random.uniform(0.1, 0.7) # Timer to control the spawning of new objects
    score = 0 # Initialize score
    score_popups = [] # Add a list to store individual score pop-ups

    last_time = time.time()

    # Main game loop
    currentstate = GAME_STATE['Playing'];
    running = True
    while running:
        if (currentstate == GAME_STATE['Playing']):
            screen.fill(const.WHITE) # take this away?
            # Set the mouse cursor to the crosshair image
            pygame.mouse.set_visible(False)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(crosshair_image, (mouse_x - crosshair_image.get_width() / 2, mouse_y - crosshair_image.get_height() / 2))


            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            c_time = pygame.time.get_ticks()
            elapsed_time = (c_time - start_time) // 1000  # Convert milliseconds to seconds
            remaining_time = max(0, const.TIME_LIMIT - elapsed_time)  # Ensure remaining_time doesn't go below 0
            
            # Draw the background image
            #background_image = change_background(score)
            
            screen.blit(background_image, (0, 0))

            if remaining_time == 0:
                currentstate = GAME_STATE['Game Over'];
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for obj in objects[:]:
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
                obj.update(dt)
                obj.draw(screen, const.DEFAULT_FONT, current_time)  # Pass the font and current time

            score_text = const.DEFAULT_FONT.render(f"Score: {int(score)}", True, const.WHITE)
            screen.blit(score_text, (10, 10))  # Display the text at (10, 10)
            #update timer
            timer_text = const.DEFAULT_FONT.render(f"Time: {remaining_time}", True, const.WHITE)
            screen.blit(timer_text, (const.screen_width//2.2, 10))  # Display the timer at (10, 10) on the screen
            
            # Render individual score popups after a hit
            for popup in score_popups[:]:
                elapsed_time = current_time - popup["timestamp"]
                if elapsed_time > 1:  # Display popup for 1 second
                    score_popups.remove(popup)
                    continue
                popup_hitscore(int(popup['score']), popup['x'], popup['y'])

            # replace cursor with crosshair
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(crosshair_image, (mouse_x - crosshair_image.get_width() / 2, mouse_y - crosshair_image.get_height() / 2))
        
            # Remove objects that have left the screen
            objects = [obj for obj in objects if obj.x >= -50 and obj.x <= const.screen_width + 50 and obj.y >= -50 and obj.y <= const.screen_height + 50]

            # Spawn a new object if fewer than 3 are present
            if len(objects) < 4 and current_time >= next_spawn_time:
                objects.append(spawn_object())
                next_spawn_time = current_time + random.uniform(0.1, 0.7)
            pygame.display.flip()  # Update the display

        elif (currentstate == GAME_STATE['Game Over']):
            hs.load_highscores()
            hs.update_highscores(score)
            currentstate = GAME_STATE['Highscore Entry']

        elif (currentstate == GAME_STATE['Highscore Entry']):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            screen.fill(const.BLACK)  # Clear the screen
            #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # get normal cursor
            pygame.mouse.set_visible(True)
            final_score_text = const.DEFAULT_FONT.render(f"Final Score: {int(score)}", True, const.WHITE)
            screen.blit(final_score_text, (const.screen_width // 6 , const.screen_height // 2 - 50))
            hs.display_highscores(pygame, screen, const.screen_width, const.screen_height)
            pygame.display.flip()  # Update the display
        

    # Print final score (You can also display this on the screen later)
    print(f"Final Score: {score}")

    # Quit Pygame
    pygame.quit()



if __name__ == "__main__":
    start_game()