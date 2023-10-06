import game_setup
import constants as const
import pygame
from game_object import AnimationObject

SCREEN = game_setup.screen


SPRITE_MASK = game_setup.sprite_mask
PLANE_L_MASK = game_setup.plane_l_mask
PLANE_R_MASK = game_setup.plane_r_mask

def popup_hitscore(score, x, y):
    # Create a text surface with a transparent background
    font = pygame.font.Font(None, 48)
    text = font.render(str(score), True, const.YELLOW, const.TRANSPARENT)

    # Get the text rect to position it
    text_rect = text.get_rect()
    text_rect.center = (x+10, y+10)

    # Blit the text surface onto the game screen
    SCREEN.blit(text, text_rect)

def is_click_on_sprite(mouse_x, mouse_y, sprite_x, sprite_y):
    # Calculate the local coordinates within the sprite
    local_x, local_y = mouse_x - sprite_x, mouse_y - sprite_y
    
    # Check if the local coordinates are within the sprite's dimensions for flying object
    if 0 <= local_x < SPRITE_MASK.get_size()[0] and 0 <= local_y < SPRITE_MASK.get_size()[1]:
        # Check if the corresponding pixel in the mask is set (collision)
        if SPRITE_MASK.get_at((local_x, local_y)):
            return 'flying_object'
    # Check if the local coordinates are within the sprite's dimensions for left going plane
    elif 0 <= local_x < PLANE_L_MASK.get_size()[0] and 0 <= local_y < PLANE_L_MASK.get_size()[1]:
        # Check if the corresponding pixel in the mask is set (collision)
        if PLANE_L_MASK.get_at((local_x, local_y)):
            return 'plane'
    # Check if the local coordinates are within the sprite's dimensions for right going plane
    elif 0 <= local_x < PLANE_R_MASK.get_size()[0] and 0 <= local_y < PLANE_R_MASK.get_size()[1]:
        # Check if the corresponding pixel in the mask is set (collision)
        if PLANE_R_MASK.get_at((local_x, local_y)):
            return 'plane'

    return False


def consume_events(score, objects, planes, score_popups, explosions, current_time):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for obj in objects[:]:
                time_elapsed = current_time - obj.timestamp
                hit = is_click_on_sprite(mouse_x, mouse_y, int(obj.x), int(obj.y))
                if (hit == 'flying_object'):
                    score_increment = int(obj.end_score + (obj.start_score - obj.end_score) * ((obj.total_time - time_elapsed) / obj.total_time))
                    objects.remove(obj)
                elif (hit == 'plane'):
                    score_increment = const.PLANE_PENALTY
                    planes.remove(obj)
                else:
                    return running, score
                score += score_increment
                # Add score popup to array
                score_popups.append({"score": score_increment, "x": mouse_x, "y": mouse_y, "timestamp": current_time})
                # Animate explosion
                explosions.append(AnimationObject(obj.x, obj.y, game_setup.VFX_EXPLOSION, x_offset=game_setup.FLYING_OBJECT_WIDTH//30, y_offset=game_setup.FLYING_OBJECT_HEIGHT//3))
    return running, score