from game_object import FlyingObject
from math import radians, cos, sin
import random
import constants as const
import game_setup

flying_object = game_setup.FLYING_OBJECT
plane_l = game_setup.PLANE_L
plane_r = game_setup.PLANE_R

# spawn new object that flies in a straight line across the screen. Apply some restrictions so that they actually cross the full screen.
def spawn_object():
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    angle_range = {
        'top': (260, 280),
        'bottom': (80, 100),
        'left': (350, 370),
        'right': (170, 190)
    }
    min_angle, max_angle = angle_range[edge]

    if edge in ['top', 'bottom']:
        initial_x = random.randint(int(0.15 * const.screen_width), int(0.85 * const.screen_width))
        initial_y = -50 if edge == 'top' else const.screen_height + 50
    else:
        initial_x = -50 if edge == 'left' else const.screen_width + 50
        initial_y = random.randint(int(0.15 * const.screen_height), int(0.85 * const.screen_height))

    angle = radians(random.uniform(min_angle, max_angle))
    speed = random.uniform(const.MIN_SPEED_FLYING_OBJECT, const.MAX_SPEED_FLYING_OBJECT)
    
    velocity = [speed * cos(angle), -speed * sin(angle)]
    
    return FlyingObject(initial_x, initial_y, flying_object, velocity, speed)

#spawn new plane that flies on a static path across the screen.
def spawn_plane(direction):
    speed = random.uniform(const.MIN_SPEED_PLANE, const.MAX_SPEED_PLANE)
    if direction == 'left':
        angle = radians(195)
        plane = plane_l
        start_x = const.screen_width+50
        start_y = random.randint(int(0.05 * const.screen_height), int(0.80 * const.screen_height))
    elif direction =='right':
        angle = radians(345)
        plane = plane_r
        start_x = -50
        start_y = random.randint(int(0.05 * const.screen_height), int(0.80 * const.screen_height))
    velocity = [speed * cos(angle), -speed * sin(angle)] 
    return FlyingObject(start_x, start_y, plane, velocity, speed)