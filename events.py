import game_setup
import pygame
from game_object import AnimationObject
import constants as const
import render
import start_screen as ss
import math


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

def consume_events(score, objects, planes, bonus_circle, score_popups, explosions, laser_shots, current_time):
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
            if bonus_circle:
                distance = math.sqrt((mouse_x - bonus_circle[0].x) ** 2 + (mouse_y - bonus_circle[0].y) ** 2)
                if distance <= bonus_circle[0].radius:
                    game_setup.time_bonus += 3
                    explosions.append(AnimationObject(bonus_circle[0].x, bonus_circle[0].y, game_setup.VFX_EXPLOSION, x_offset=80, y_offset=100, size_modifier=0.5))
                    bonus_circle.pop(0)
                    # We should not be penalized if we shoot a bonus on top of a plane, so just return if we hit a bonus
                    return
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
                return False
            elif event.key == pygame.K_RETURN: #Return character starts game
                game_setup.CurrentState = game_setup.GameState['Playing']
                game_setup.start_time = pygame.time.get_ticks()
                print("Start button clicked!")
                return True
            elif event.key == pygame.K_BACKSPACE:
                ss.eraseActiveString()
            elif 32 <= event.key <= 126: #accept printable characters as input
                ss.appendActiveString(event.unicode)
            elif event.key == pygame.K_TAB:
                ss.switchActiveBox()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if ss.clear_name_x <= mouse_x <= ss.clear_name_x + game_setup.clear_img_w and ss.clear_name_y <= mouse_y <= ss.clear_name_y + game_setup.clear_img_h:
                game_setup.user_name = ''
            if ss.name_rect.collidepoint(event.pos):
                ss.switchActiveBox('name')
            if ss.clear_email_x <= mouse_x <= ss.clear_email_x + game_setup.clear_img_w and ss.clear_email_y <= mouse_y <= ss.clear_email_y + game_setup.clear_img_h:
                game_setup.user_email = ''
            if ss.email_rect.collidepoint(event.pos):
                ss.switchActiveBox('email')
            
                
                # Handle the Start button click
                print("Start button clicked!")
                print(f"Name: {game_setup.user_name}")
                print(f"Email: {game_setup.user_name}")
    return running