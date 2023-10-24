import constants as const
import game_setup
import pygame
import start_screen as ss
import endscreen as es
import highscores as hs


SCREEN = game_setup.screen

def render_objects(objects, current_time, dt):
    for obj in objects:
        obj.update(dt)
        obj.draw(SCREEN, const.DEFAULT_FONT, current_time)  # Pass the font and current time

def render_score(score):
    score_text = const.DEFAULT_FONT.render(f"Score: {int(score)}", True, const.WHITE)
    SCREEN.blit(score_text, (10, 10))

def render_timer(remaining_time):
    timer_color = const.RED
    if remaining_time > 20:
        timer_color = const.GREEN
    elif remaining_time > 10:
        timer_color = const.YELLOW
    
    timer_text = const.DEFAULT_FONT.render(f"Time: {remaining_time}", True, timer_color)
    SCREEN.blit(timer_text, (const.screen_width//2.3, 40))


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
        

def render_end_page(score):
    font = pygame.font.SysFont(None, 55)
    SCREEN.fill(const.BLACK)  # Clear the screen
    #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # get normal cursor
    pygame.mouse.set_visible(True)

    # background
    SCREEN.blit(game_setup.esbg_img, (0, 0))

     #logo image
    SCREEN.blit(game_setup.logo_img, (70, 70))

    #plane and stone
    SCREEN.blit(game_setup.plane_stone_img, (es.plane_stone_x, es.plane_stone_y))
    
    # Restart button
    SCREEN.blit(game_setup.restart_img, (es.restart_img_x, es.restart_img_y))
    
    # Player score
    SCREEN.blit(game_setup.score_img, (es.score_rect_x, es.score_rect_y))
    font_score = pygame.font.SysFont(None, int(game_setup.score_img.get_height() * 0.8))
    score_text = font_score.render(f"{int(score)}", True, const.WHITE)
    SCREEN.blit(score_text, (es.score_rect_x + 60, es.score_rect_y + 50))
    name_text = font.render(f"{game_setup.user_name}", True, const.WHITE)
    SCREEN.blit(name_text, (es.score_rect_x + int(game_setup.score_img.get_width() * 0.45), es.score_rect_y + 100))
    
    # Highscore
    SCREEN.blit(game_setup.hs_rect_es, (es.hs_rect_es_x, es.hs_rect_es_y))
    hs.display_highscores(es.hs_rect_es_x + game_setup.hs_rect_es.get_width() / 2, es.hs_rect_es_y + 30, 1.20 * es.hs_rect_es_x, es.hs_rect_es_y + 140, 1)

  



def render_animations(animations):
    remaining_animations = []
    for animation in animations:
        done = animation.draw(SCREEN)
        if not done:
            remaining_animations.append(animation)
    
    return remaining_animations

def render_start_screen():
    SCREEN.blit(game_setup.ss_background_image, (0, 0))

    base_font = pygame.font.Font(None, 28)
    text_rect_color_inactive = pygame.Color('gray78')
    text_rect_color_active = pygame.Color('whitesmoke')
    text_color = pygame.Color('orchid3')
    text_fill_color = pygame.Color('gray80')


    #logo image
    SCREEN.blit(game_setup.logo_img, (70, 70))

     # Highscore
    hs_rect_x = const.screen_width * 0.33
    hs_rect_y = const.screen_height * 0.3
    SCREEN.blit(game_setup.hs_rect, (hs_rect_x, hs_rect_y))
    SCREEN.blit(game_setup.hs_trophy, (hs_rect_x + game_setup.hs_rect.get_width() / 2 - game_setup.hs_trophy.get_width() / 2, hs_rect_y - game_setup.hs_trophy.get_height()-10))
    hs.display_highscores(hs_rect_x + game_setup.hs_rect.get_width() / 2, hs_rect_y + 40, 1.1 * hs_rect_x, hs_rect_y + 140)

    #Name box
    if ss.name_rect_active:
        pygame.draw.rect(SCREEN,text_rect_color_active,ss.name_rect,3)
    else:
        pygame.draw.rect(SCREEN,text_rect_color_inactive,ss.name_rect,1)
    text_surface = base_font.render(game_setup.user_name, True, text_color)
    SCREEN.blit(text_surface,(ss.name_rect.x + 10, ss.name_rect.y + 10))
    #ss.name_rect.w = max(ss.name_rect_width, text_surface.get_width() + 70)
    #Name string relative to box
    nametext = base_font.render('Name:', True, (255, 255, 255))
    SCREEN.blit(nametext, (ss.name_rect_x, ss.name_rect_y-30))
    #clear icon
    ss.clear_name_x = ss.name_rect.x + ss.name_rect.w - 45
    ss.clear_name_y = ss.name_rect.y + 1
    SCREEN.blit(game_setup.clear_img, (ss.clear_name_x, ss.clear_name_y))

    #Email box, handle long emails
    text_surface = base_font.render(game_setup.user_email, True, text_color)
    if ss.email_rect_active:
        pygame.draw.rect(SCREEN,text_rect_color_active,ss.email_rect,3)
    else:
        pygame.draw.rect(SCREEN,text_rect_color_inactive,ss.email_rect,1)
    SCREEN.blit(text_surface,(ss.email_rect.x + 10, ss.email_rect.y + 10))
    ss.email_rect.w = max(ss.email_rect_width, text_surface.get_width() + 70)
    # Email string relative to box
    emailtext = base_font.render('Email:', True, (255, 255, 255))
    SCREEN.blit(emailtext, (ss.email_rect_x, ss.email_rect_y-30))
    #clear icon
    ss.clear_email_x = ss.email_rect.x + ss.email_rect.w - 45
    ss.clear_email_y = ss.email_rect.y + 1
    SCREEN.blit(game_setup.clear_img, (ss.clear_email_x, ss.clear_email_y))

   
    # Start button
    SCREEN.blit(game_setup.start_img, (ss.start_img_x, ss.start_img_y))
    
    



