import math
import pygame
import game_setup

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


def display_highscores(hs_x_center, hs_y, entries_x, entries_y):
    # Sort the highscores by score in descending order
    highscores = load_highscores()
    highscores.sort(key=lambda x: x[0], reverse=True)
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
        score_text = font.render(f"{i+1} {'.':<4} {int(entry[0]):<8} {entry[1]}", True, color)
        game_setup.screen.blit(score_text, (entries_x , entries_y + 35 * i))
    

def update_highscores(player_score):
    highscores = load_highscores()
    if game_setup.user_name == '' and game_setup.user_email == '':
        highscores.append((int(player_score), 'anonymous', 'anonymous'))
    elif game_setup.user_email == '':
        highscores.append((int(player_score), game_setup.user_name, 'anonymous'))
    elif game_setup.user_name == '':
        highscores.append((int(player_score), 'anonymous', game_setup.user_email))
    else:
        highscores.append((int(player_score), game_setup.user_name, game_setup.user_email))
    #print(highscores)
    highscores.sort(key=lambda x: x[0], reverse=True)
    #highscores = highscores[:10]  # Keep only the top 10 highscores
    #print(highscores)
    save_highscores(highscores)



