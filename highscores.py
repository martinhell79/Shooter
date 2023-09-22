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
    hs_text = font.render('HIGHSCORE', True, (255, 255, 255))
    screen.blit(hs_text, (3 * width // 5 , height // 2 - 100))
    # Display the top 5 highscores
    font = pygame.font.SysFont(None, 36)  # Default font, size 36
    for i, entry in enumerate(sorted_highscores[:5]):
        score_text = font.render(f"{i+1}. {int(entry['score'])}", True, (255, 255, 255))
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
