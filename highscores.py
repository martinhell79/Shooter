import math
import pygame
import game_setup
import constants as const
import endscreen

highscore = []
highscore_loaded = False

def load_highscores():
    highscores = []
    try:
        with open("highscores.txt", "r") as file:
            highscores_data = file.readlines()
        for line in highscores_data:
            if line:
                score, name, email = line.strip().split("\ ")
                highscores.append((int(score), name, email))
    except FileNotFoundError:
        pass  # Handle the case where the file doesn't exist yet
    return highscores
    #print(highscores)


def save_highscores(highscores):
    with open("highscores.txt", "w") as file:
        for score, name, email in highscores:
            file.write(f"{score}\ {name}\ {email}\n")


def display_highscores(highscores, hs_x_center, hs_y, entries_x, entries_y, highlight_current = 0):
    # Sort the highscores by score in descending order
    #highscores = load_highscores()
    highscores.sort(key=lambda x: x[0], reverse=True)
    index = -1
    if highlight_current:
        index = get_index(highscores, (game_setup.score, game_setup.user_name, game_setup.user_email))
        #print(f'index: {index}')
    
    #print(highscores)
    font = pygame.font.SysFont(None, 70)  # Default font, size 36
    
    time_elapsed = pygame.time.get_ticks() / 1000
    color = (255,255,255)
    color_change_speed = 6
    r = int(255 * abs(math.sin(time_elapsed * color_change_speed)))
    g = int(255 * abs(math.sin(time_elapsed * color_change_speed + 2 * math.pi / 3)))
    b = int(255 * abs(math.sin(time_elapsed * color_change_speed + 4 * math.pi / 3)))
    color = (r, g, b)
    hs_text = font.render('HIGHSCORE', True, color)
    game_setup.screen.blit(hs_text, (hs_x_center - hs_text.get_width() / 2, hs_y))

    
    
    # Display the top 5 highscores
    font = pygame.font.SysFont(None, 44)  # Default font, size 36
    # color = [(255,0,0),(0,255,0),(0,0,255),(128,128,128),(100,200,250)]
    color_change_speed = [6,6,7,7,8,8,9,9,10,10]
    for i, entry in enumerate(highscores[:10]):
        time_elapsed = (pygame.time.get_ticks() / 1000) + 5*i
        r = int(100 + 80 * abs(math.sin(time_elapsed * color_change_speed[i])))
        g = int(170 + 80 * abs(math.sin(time_elapsed * color_change_speed[i] + 2 * math.pi / 3)))
        b = int(170 + 80 * abs(math.sin(time_elapsed * color_change_speed[i] + 4 * math.pi / 3)))
        color = (r, g, b)
        score_text_1 = font.render(f"{i+1}.", True, color)
        score_text_2 = font.render(f"{int(entry[0]):>}", True, color)
        score_text_3 = font.render(f"{entry[1]:<}", True, color)
        game_setup.screen.blit(score_text_1, (entries_x , entries_y + 40 * i))
        game_setup.screen.blit(score_text_2, (entries_x + 100, entries_y + 40 * i))
        game_setup.screen.blit(score_text_3, (entries_x + 230, entries_y + 40 * i))
        if i == index:
            r = pygame.Rect(endscreen.hs_rect_es_x + 30, entries_y + 40 * i - 5, game_setup.hs_rect_es.get_width() - 60, score_text_3.get_rect().height + 10)
            pygame.draw.rect(game_setup.screen,(233,108,169),r,4)
            print('draw rect')
    

def update_highscores(player_score):
    highscores = load_highscores()
    highscores.append((int(player_score), game_setup.user_name, game_setup.user_email))
    #print(highscores)
    highscores.sort(key=lambda x: x[0], reverse=True)
    
    #highscores = highscores[:10]  # Keep only the top 10 highscores
    #print(highscores)
    save_highscores(highscores)


def get_index(highscores, tuple):
    return next((i for i, x in enumerate(highscores) if x == tuple), -1)
    
def get_email_occurences(email):
    highscores = load_highscores()
    return len([a[2] for a in highscores if a[2] == email])
    