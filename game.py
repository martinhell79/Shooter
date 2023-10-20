import pygame
import random
import time
import constants as const
import highscores as hs
import game_setup
import spawn
import events
import render


GAME_STATE = game_setup.GameState
SCREEN = game_setup.screen
time_bonus = 0
background_image = game_setup.background_image
crosshair_image = game_setup.crosshair_image
hotspot = game_setup.hotspot
plane_l = game_setup.PLANE_L
plane_r = game_setup.PLANE_R



def start_game(time_limit=30):
    #Gameplay variables
    remaining_time = time_limit
    #planes = game_setup.planes #[spawn.spawn_plane() for _ in range(1)] # Lets start with one plane
    #objects = game_setup.objects #[spawn.spawn_object() for _ in range(4)] # Initialize the first object and object list
    bonus_circle = game_setup.bonus_circle
    next_spawn_time = time.time() + random.uniform(0.1, 0.7) # Timer to control the spawning of new objects
    score_popups = [] # Add a list to store individual score pop-ups
    explosions = []
    laser_shots = []

    
    #last_time = game_setup.last_time
    # Main game loop
    game_setup.CurrentState = GAME_STATE['Start_Screen'];
    running = True
    while running:
        if (game_setup.CurrentState == GAME_STATE['Start_Screen']):
            render.render_start_screen()
            running = events.startScreenEvents()
            pygame.display.flip()

        elif (game_setup.CurrentState == GAME_STATE['Playing']):
            SCREEN.blit(background_image, (0, 0))
            SCREEN.blit(game_setup.planet1, (50,50))
            SCREEN.blit(game_setup.planet2, (const.screen_width - 450, 100))
            SCREEN.blit(game_setup.planet3, (170, const.screen_height - 300))
            render.render_cursor(crosshair_image)
            
            current_time = time.time()
            dt = current_time - game_setup.last_time
            game_setup.last_time = current_time
            
            c_time = pygame.time.get_ticks()
            elapsed_time = (c_time - game_setup.start_time) // 1000  # Convert milliseconds to seconds
            remaining_time = max(0, time_limit - elapsed_time + game_setup.time_bonus)  # Ensure remaining_time doesn't go below 0
            if remaining_time == 0:
                game_setup.CurrentState = GAME_STATE['Game_Over']
            
            running, score = events.consume_events(game_setup.objects, game_setup.planes, bonus_circle, score_popups, explosions, laser_shots, current_time)
            
            render.render_objects(game_setup.objects + game_setup.planes + bonus_circle, current_time=current_time, dt=dt)

            render.render_score(score)
            render.render_timer(remaining_time)
            render.render_score_popups(score_popups, current_time=current_time)

            render.render_cursor(crosshair_image)

            explosions = render.render_animations(explosions)
            laser_shots = render.render_animations(laser_shots)

            # Remove objects that have left the screen
            game_setup.objects = [obj for obj in game_setup.objects if obj.x >= -50 and obj.x <= const.screen_width + 50 and obj.y >= -50 and obj.y <= const.screen_height + 50]
            game_setup.planes = [plane for plane in game_setup.planes if plane.x > -50 and plane.x <= const.screen_width + 50 and plane.y >= -50 and plane.y <= const.screen_height + 50]
            
            # remove bonus circles if lifespan has passed
            bonus_circle = [bs for bs in bonus_circle if bs.elapsed_time < bs.lifespan]

            # Spawn a new object if fewer than 4 are present
            if len(game_setup.objects) < 4 and current_time >= next_spawn_time:
                game_setup.objects.append(spawn.spawn_object())
                next_spawn_time = current_time + random.uniform(0.1, 0.7)
            if len(game_setup.planes) < 1:
                game_setup.planes.append(spawn.spawn_plane())
            if game_setup.spawn_time_circles and elapsed_time >= game_setup.spawn_time_circles[0]:
                bonus_circle.append(spawn.spawn_time_adder())
                game_setup.spawn_time_circles.pop(0)


            pygame.display.flip()  # Update the display

        elif (game_setup.CurrentState == GAME_STATE['Game_Over']):
            hs.load_highscores()
            print(f'score: {score}')
            print(f'game_setup.score: {game_setup.score}')
            hs.update_highscores(score)
            game_setup.CurrentState = GAME_STATE['Highscore_Entry']

        elif (game_setup.CurrentState == GAME_STATE['Highscore_Entry']):
            running = render.render_highscore_page(score)
            running = events.endPageEvents()
        
        else:
            print('No matching game state - quitting')
            running = False

    #print(f"Final Score: {score}")
    pygame.quit()



if __name__ == "__main__":
    start_game(10)