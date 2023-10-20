import constants as const
import game_setup
import pygame
import start_screen as ss

import highscores as hs

SCREEN = game_setup.screen

def render_objects(objects, current_time, dt):
    for obj in objects:
        obj.update(dt)
        obj.draw(SCREEN, const.DEFAULT_FONT, current_time)  # Pass the font and current time

def render_score(score):
    score_text = const.DEFAULT_FONT.render(f"Score: {int(score)}", True, const.WHITE)
    SCREEN.blit(score_text, (10, 10))  # Display the text at (10, 10)

def render_timer(remaining_time):
    timer_text = const.DEFAULT_FONT.render(f"Time: {remaining_time}", True, const.WHITE)
    SCREEN.blit(timer_text, (const.screen_width//2.1, 40))  # Display the timer at (10, 10) on the screen


def popup_hitscore(score, x, y):
    # Create a text surface with a transparent background
    font = pygame.font.Font(None, 48)
    text = font.render(str(score), True, const.YELLOW, const.TRANSPARENT)

    # Get the text rect to position it
    text_rect = text.get_rect()
    text_rect.center = (x+10, y+10)

    # Blit the text surface onto the game screen
    SCREEN.blit(text, text_rect)


def render_score_popups(score_popups, current_time):
    # Render individual score popups after a hit
    for popup in score_popups[:]:
        elapsed_time = current_time - popup["timestamp"]
        if elapsed_time > 1:  # Display popup for 1 second
            score_popups.remove(popup)
            continue
        popup_hitscore(int(popup['score']), popup['x'], popup['y'])


def render_cursor(crosshair_image):
    pygame.mouse.set_visible(False)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    SCREEN.blit(crosshair_image, (mouse_x - crosshair_image.get_width() / 2, mouse_y - crosshair_image.get_height() / 2))
        

def render_highscore_page(score):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    font = pygame.font.SysFont(None, 55)
    SCREEN.fill(const.BLACK)  # Clear the screen
    #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # get normal cursor
    pygame.mouse.set_visible(True)
    score_x = const.screen_width // 6 - 50
    score_y = const.screen_height // 2 - 50

    SCREEN.blit(game_setup.hand_img, (score_x, score_y + 50))

    score_text = font.render(f"Score: {int(score)}", True, const.WHITE)
    SCREEN.blit(score_text, (score_x + 20, score_y))
    hs.display_highscores(pygame, SCREEN, const.screen_width, const.screen_height)
    pygame.display.flip()  # Update the display
    return running


def render_animations(animations):
    remaining_animations = []
    for animation in animations:
        done = animation.draw(SCREEN)
        if not done:
            remaining_animations.append(animation)
    
    return remaining_animations

def render_start_screen():
    SCREEN.blit(game_setup.ss_background_image, (0, 0))

    base_font = pygame.font.Font(None, 32)
    text_rect_color_inactive = pygame.Color('gray78')
    text_rect_color_active = pygame.Color('whitesmoke')
    text_color = pygame.Color('orchid3')
    text_fill_color = pygame.Color('gray80')


    #logo image
    SCREEN.blit(game_setup.logo_img, (70, 70))

    #Name box
    if ss.name_rect_active:
        pygame.draw.rect(SCREEN,text_rect_color_active,ss.name_rect,3)
    else:
        pygame.draw.rect(SCREEN,text_rect_color_inactive,ss.name_rect,1)
    text_surface = base_font.render(game_setup.user_name, True, text_color)
    SCREEN.blit(text_surface,(ss.name_rect.x + 10, ss.name_rect.y + 10))
    ss.name_rect.w = max(ss.name_rect_width, text_surface.get_width() + 70)
    #Name string relative to box
    nametext = base_font.render('Name:', True, (255, 255, 255))
    SCREEN.blit(nametext, (ss.name_rect_x, ss.name_rect_y-30))
    #clear icon
    ss.clear_name_x = ss.name_rect.x + ss.name_rect.w - 45
    ss.clear_name_y = ss.name_rect.y + 1
    SCREEN.blit(game_setup.clear_img, (ss.clear_name_x, ss.clear_name_y))

    #Email box
    if ss.email_rect_active:
        pygame.draw.rect(SCREEN,text_rect_color_active,ss.email_rect,3)
    else:
        pygame.draw.rect(SCREEN,text_rect_color_inactive,ss.email_rect,1)
    text_surface = base_font.render(game_setup.user_email, True, text_color)
    SCREEN.blit(text_surface,(ss.email_rect.x + 10, ss.email_rect.y + 10))
    ss.email_rect.w = max(ss.email_rect_width, text_surface.get_width() + 70)
    # Email string relative to box
    emailtext = base_font.render('Email:', True, (255, 255, 255))
    SCREEN.blit(emailtext, (ss.email_rect_x, ss.email_rect_y-30))
    #clear icon
    ss.clear_email_x = ss.email_rect.x + ss.email_rect.w - 45
    ss.clear_email_y = ss.email_rect.y + 1
    SCREEN.blit(game_setup.clear_img, (ss.clear_email_x, ss.clear_email_y))

    
    



