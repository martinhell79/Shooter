import constants as const
import game_setup
import events
import pygame
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
    SCREEN.blit(timer_text, (const.screen_width//2.2, 10))  # Display the timer at (10, 10) on the screen

def render_score_popups(score_popups, current_time):
    # Render individual score popups after a hit
    for popup in score_popups[:]:
        elapsed_time = current_time - popup["timestamp"]
        if elapsed_time > 1:  # Display popup for 1 second
            score_popups.remove(popup)
            continue
        events.popup_hitscore(int(popup['score']), popup['x'], popup['y'])


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

    SCREEN.fill(const.BLACK)  # Clear the screen
    #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # get normal cursor
    pygame.mouse.set_visible(True)
    final_score_text = const.DEFAULT_FONT.render(f"Final Score: {int(score)}", True, const.WHITE)
    SCREEN.blit(final_score_text, (const.screen_width // 6 , const.screen_height // 2 - 50))
    hs.display_highscores(pygame, SCREEN, const.screen_width, const.screen_height)
    pygame.display.flip()  # Update the display
    return running


def render_explosions(explosions):
    remaining_explosions = []
    for explosion in explosions:
        done = explosion.draw(SCREEN)
        if not done:
            remaining_explosions.append(explosion)
    
    return remaining_explosions