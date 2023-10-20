import math

def load_highscores():
    try:
        with open("highscores.txt", "r") as file:
            highscores_data = file.readlines()

        for line in highscores_data:
            score = line.strip()
            highscores.append({"score": int(score)})
    except FileNotFoundError:
        pass  # Handle the case where the file doesn't exist yet
    #print(highscores)


def save_highscores():
    with open("highscores.txt", "w") as file:
        for entry in highscores:
            file.write(f"{entry['score']}\n")


def display_highscores(pygame, screen, width, height):
    # Sort the highscores by score in descending order
    sorted_highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)

    font = pygame.font.SysFont(None, 55)  # Default font, size 36
    
    time_elapsed = pygame.time.get_ticks() / 1000
    color = (255,255,255)
    color_change_speed = 6
    r = int(255 * abs(math.sin(time_elapsed * color_change_speed)))
    g = int(255 * abs(math.sin(time_elapsed * color_change_speed + 2 * math.pi / 3)))
    b = int(255 * abs(math.sin(time_elapsed * color_change_speed + 4 * math.pi / 3)))
    color = (r, g, b)
    hs_text = font.render('HIGHSCORE', True, color)
    screen.blit(hs_text, (3 * width // 5 , height // 2 - 100))

    
    
    # Display the top 5 highscores
    font = pygame.font.SysFont(None, 36)  # Default font, size 36
    # color = [(255,0,0),(0,255,0),(0,0,255),(128,128,128),(100,200,250)]
    color_change_speed = [3,4,5,6,7]
    for i, entry in enumerate(sorted_highscores[:5]):
        time_elapsed = (pygame.time.get_ticks() / 1000) + i
        r = int(100 + 80 * abs(math.sin(time_elapsed * color_change_speed[i])))
        g = int(150 + 80 * abs(math.sin(time_elapsed * color_change_speed[i] + 2 * math.pi / 3)))
        b = int(150 + 80 * abs(math.sin(time_elapsed * color_change_speed[i] + 4 * math.pi / 3)))
        color = (r, g, b)
        score_text = font.render(f"{i+1}. {int(entry['score'])}", True, color)
        screen.blit(score_text, (3 * width // 5 , height // 2 - 50 + 30 * i))
    

def update_highscores(player_score):
    global highscores
    highscores.append({"score": int(player_score)})
    highscores.sort(key=lambda x: x["score"], reverse=True)
    highscores = highscores[:5]  # Keep only the top 5 highscores
    print(highscores)
    save_highscores()



# Highscores data structure (if needed)
highscores = []
