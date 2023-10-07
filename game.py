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
start_time = game_setup.start_time

background_image = game_setup.background_image
crosshair_image = game_setup.crosshair_image
hotspot = game_setup.hotspot
plane_l = game_setup.PLANE_L
plane_r = game_setup.PLANE_R



def start_game(time_limit=30):
    #Gameplay variables
    remaining_time = time_limit
    planes = [spawn.spawn_plane() for _ in range(1)] # Lets start with one plane
    objects = [spawn.spawn_object() for _ in range(4)] # Initialize the first object and object list
    next_spawn_time = time.time() + random.uniform(0.1, 0.7) # Timer to control the spawning of new objects
    score = 0 # Initialize score
    score_popups = [] # Add a list to store individual score pop-ups
    explosions = []
    laser_shots = []

    last_time = time.time()

    # Main game loop
    currentstate = GAME_STATE['Playing'];
    running = True
    while running:
        if (currentstate == GAME_STATE['Start_Screen']):
            render.render_start_screen()
            running = events.startScreenEvents()
            pygame.display.flip()

        if (currentstate == GAME_STATE['Playing']):
            SCREEN.blit(background_image, (0, 0))
            render.render_cursor(crosshair_image)

            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            c_time = pygame.time.get_ticks()
            elapsed_time = (c_time - start_time) // 1000  # Convert milliseconds to seconds
            remaining_time = max(0, time_limit - elapsed_time)  # Ensure remaining_time doesn't go below 0
            if remaining_time == 0:
                currentstate = GAME_STATE['Game_Over']
            
            running, score = events.consume_events(score, objects, planes, score_popups, explosions, laser_shots, current_time)
            
            render.render_objects(objects + planes, current_time=current_time, dt=dt)

            render.render_score(score)
            render.render_timer(remaining_time)
            render.render_score_popups(score_popups, current_time=current_time)

            render.render_cursor(crosshair_image)

            explosions = render.render_animations(explosions)
            laser_shots = render.render_animations(laser_shots)

            # Remove objects that have left the screen
            objects = [obj for obj in objects if obj.x >= -50 and obj.x <= const.screen_width + 50 and obj.y >= -50 and obj.y <= const.screen_height + 50]
            planes = [plane for plane in planes if plane.x > -50 and plane.x <= const.screen_width + 50 and plane.y >= -50 and plane.y <= const.screen_height + 50]

            # Spawn a new object if fewer than 4 are present
            if len(objects) < 4 and current_time >= next_spawn_time:
                objects.append(spawn.spawn_object())
                next_spawn_time = current_time + random.uniform(0.1, 0.7)
            if len(planes) < 1:
                planes.append(spawn.spawn_plane())

            pygame.display.flip()  # Update the display

        elif (currentstate == GAME_STATE['Game_Over']):
            hs.load_highscores()
            hs.update_highscores(score)
            currentstate = GAME_STATE['Highscore_Entry']

        elif (currentstate == GAME_STATE['Highscore_Entry']):
            running = render.render_highscore_page(score)
        

    print(f"Final Score: {score}")
    pygame.quit()



if __name__ == "__main__":
    start_game()