import game_setup
import pygame
from game_object import AnimationObject
import constants as const
import render
import start_screen as ss

SCREEN = game_setup.screen

def is_click_on_sprite(mouse_x, mouse_y, sprite_x, sprite_y, image):
    mask = pygame.mask.from_surface(image)
    # Calculate the local coordinates within the sprite
    local_x, local_y = mouse_x - sprite_x, mouse_y - sprite_y
    
    # Check if the local coordinates are within the sprite's dimensions for flying object
    if 0 <= local_x < mask.get_size()[0] and 0 <= local_y < mask.get_size()[1]:
        # Check if the corresponding pixel in the mask is set (collision)
        if mask.get_at((local_x, local_y)):
            return 1
    return False

def consume_events(score, objects, planes, score_popups, explosions, laser_shots, current_time):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            laser_shots.append(AnimationObject(mouse_x, mouse_y, images=game_setup.VFX_LASER, x_offset=game_setup.FLYING_OBJECT_WIDTH//17, y_offset=game_setup.FLYING_OBJECT_HEIGHT//12,size_modifier=0.07))
            for obj in objects[:]:
                time_elapsed = current_time - obj.timestamp
                if (is_click_on_sprite(mouse_x, mouse_y, int(obj.x), int(obj.y), obj.image)):
                    score_increment = int(obj.end_score + (obj.start_score - obj.end_score) * ((obj.total_time - time_elapsed) / obj.total_time))
                    objects.remove(obj)
                    score += score_increment
                # Add score popup to array
                    score_popups.append({"score": score_increment, "x": mouse_x, "y": mouse_y, "timestamp": current_time})
                # Animate explosion
                    explosions.append(AnimationObject(obj.x, obj.y, game_setup.VFX_EXPLOSION, x_offset=game_setup.FLYING_OBJECT_WIDTH//30, y_offset=game_setup.FLYING_OBJECT_HEIGHT//3))
            for pl in planes[:]:  
                time_elapsed = current_time - pl.timestamp    
                print(f'x: {pl.x} y: {pl.y} mx: {mouse_x} my: {mouse_y}') 
                if (is_click_on_sprite(mouse_x, mouse_y, int(pl.x), int(pl.y), pl.image)):
                    score_increment = const.PLANE_PENALTY
                    planes.remove(pl)
                    score += score_increment
                    # Add score popup to array
                    score_popups.append({"score": score_increment, "x": mouse_x, "y": mouse_y, "timestamp": current_time})
                    # Animate explosion (same for all planes currently)
                    explosions.append(AnimationObject(pl.x, pl.y, game_setup.VFX_EXPLOSION, x_offset=game_setup.PLANE_L_WIDTH//5, y_offset=game_setup.PLANE_L_HEIGHT))
    return running, score

def startScreenEvents():
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_BACKSPACE:
                game_setup.user_name = game_setup.user_name[:-1]
            else:
                game_setup.user_name += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ss.name_rect.collidepoint(event.pos):
                # Handle the Start button click
                print("Start button clicked!")
                print(f"Name: {game_setup.user_name}")
                print(f"Email: {game_setup.user_name}")
    return running