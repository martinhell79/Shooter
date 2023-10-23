import game_setup
import pygame
from game_object import AnimationObject
import constants as const
import start_screen as ss
import endscreen as es
import math
import time
import random
from game_setup import SOUND_LASER, SOUND_EXPLOSION, SOUND_TIME_EXTENSION
import highscores as hs


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

def consume_events(objects, planes, bonus_circle, score_popups, explosions, laser_shots, current_time):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            _consume_shoot_event(objects, planes, bonus_circle, score_popups, explosions, laser_shots, current_time, running)

    return running, game_setup.score


def _consume_shoot_event(objects, planes, bonus_circle, score_popups, explosions, laser_shots, current_time, running):
    pygame.mixer.Sound.play(SOUND_LASER)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    laser_shots.append(AnimationObject(mouse_x, mouse_y, images=game_setup.VFX_LASER, x_offset=14, y_offset=12,size_modifier=0.07))
    if bonus_circle:
        if (is_click_on_sprite(mouse_x, mouse_y, int(bonus_circle[0].x), int(bonus_circle[0].y), bonus_circle[0].image)):
            pygame.mixer.Sound.play(SOUND_TIME_EXTENSION)
            game_setup.time_bonus += const.BONUS_TIME
            explosions.append(AnimationObject(bonus_circle[0].x, bonus_circle[0].y, game_setup.VFX_EXPLOSION, x_offset=10, y_offset=10, size_modifier=0.5))
            bonus_circle.pop(0)
            # We should not be penalized if we shoot a bonus on top of a plane, so just return if we hit a bonus
            return running, game_setup.score
        
    shot_hit_object = False
    for obj in objects[:]:
        time_elapsed = current_time - obj.timestamp
        if (is_click_on_sprite(mouse_x, mouse_y, int(obj.x), int(obj.y), obj.image)):
            score_increment = int(obj.end_score + (obj.start_score - obj.end_score) * ((obj.total_time - time_elapsed) / obj.total_time))
            objects.remove(obj)
            game_setup.score += score_increment
            shot_hit_object = True
            # Add score popup to array
            score_popups.append({"score": score_increment, "x": mouse_x, "y": mouse_y, "timestamp": current_time})
            # Animate explosion
            explosions.append(AnimationObject(obj.x, obj.y, game_setup.VFX_EXPLOSION, x_offset=70, y_offset=70))
    
    for pl in planes[:]:  
        time_elapsed = current_time - pl.timestamp    
        print(f'x: {pl.x} y: {pl.y} mx: {mouse_x} my: {mouse_y}') 
        if (is_click_on_sprite(mouse_x, mouse_y, int(pl.x), int(pl.y), pl.image)):
            score_increment = const.PLANE_PENALTY
            planes.remove(pl)
            game_setup.score += score_increment
            # Add score popup to array
            score_popups.append({"score": score_increment, "x": mouse_x, "y": mouse_y, "timestamp": current_time})
            # Animate explosion (same for all planes currently)
            explosions.append(AnimationObject(pl.x, pl.y, game_setup.VFX_EXPLOSION, x_offset=game_setup.PLANE_L_WIDTH//30, y_offset=game_setup.PLANE_L_HEIGHT//3))
            shot_hit_object = True
            
    if shot_hit_object:
        pygame.mixer.Sound.play(SOUND_EXPLOSION)

    return running


def startScreenEvents():
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_RETURN: #Return character starts game                
                init_play()
                return True
            elif event.key == pygame.K_BACKSPACE:
                ss.eraseActiveString()
            elif event.unicode in const.ALLOWED_CHARS: #accept printable characters as input
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
            if ss.start_img_x <= mouse_x <= ss.start_img_x + game_setup.start_img.get_width() and ss.start_img_y <= mouse_y <= ss.start_img_y + game_setup.start_img.get_height():
                if hs.get_email_occurences(game_setup.user_email) < 5 or game_setup.user_email == 'Anonymous':
                    init_play()
                    return True
                # Handle the Start button click
                print("Start button clicked!")
                print(f"Name: {game_setup.user_name}")
                print(f"Email: {game_setup.user_name}")
    return running


def endPageEvents():
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_RETURN: #Return character re-initializes game
                game_setup.CurrentState = game_setup.GameState['Start_Screen']
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if es.restart_img_x <= mouse_x <= es.restart_img_x + game_setup.restart_img.get_width() and es.restart_img_y <= mouse_y <= es.restart_img_y + game_setup.restart_img.get_height():
                game_setup.CurrentState = game_setup.GameState['Start_Screen']
    return running


def init_play():
    game_setup.CurrentState = game_setup.GameState['Playing']
    game_setup.start_time = pygame.time.get_ticks()
    game_setup.time_bonus = 0
    game_setup.score = 0
    game_setup.last_time = time.time()
    game_setup.planes = [] #[spawn.spawn_plane() for _ in range(1)]
    game_setup.objects = [] #[spawn.spawn_object() for _ in range(4)]
    game_setup.bonus_circle = []
    game_setup.spawn_time_circles = [8 + random.randint(0, 4), 18 + random.randint(0, 5), 31 + random.randint(0, 1)]
    game_setup.user_name = game_setup.user_name or 'Anonymous'
    game_setup.user_email = game_setup.user_email or 'Anonymous'
    pass
                