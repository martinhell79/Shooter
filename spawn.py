from game_object import FlyingObject, TimedObject
from math import radians, cos, sin
import random
import constants as const
import game_setup

flying_objects = game_setup.flying_objects
#flying_object_r = game_setup.FLYING_OBJECT_R
plane_l = game_setup.PLANE_L
plane_r = game_setup.PLANE_R

# spawn new object that flies in a straight line across the screen. Apply some restrictions so that they actually cross the full screen.
def spawn_object():
    edge = random.choice(['top_l', 'top_r', 'bottom_l', 'bottom_r', 'left_b', 'left_t', 'right_b', 'right_t'])
    delta = 25
    angle_range = {
        'top_l': (270+delta, 360-delta),
        'bottom_l': (0+delta, 90-delta),
        'left_b': (0+delta, 90-delta),
        'right_b': (90+delta, 180-delta),
        'top_r': (180+delta, 270-delta),
        'bottom_r': (90+delta, 180-delta),
        'left_t': (270+delta, 360-delta),
        'right_t': (180+delta, 270-delta)
    }
    min_angle, max_angle = angle_range[edge]

    if edge in ['top_l', 'bottom_l']:
        initial_x = random.randint(int(0.05 * const.screen_width), int(0.45 * const.screen_width))
        initial_y = -50 if edge == 'top_l' else const.screen_height + 50
    elif edge in ['top_r', 'bottom_r']:
        initial_x = random.randint(int(0.55 * const.screen_width), int(0.95 * const.screen_width))
        initial_y = -50 if edge == 'top_r' else const.screen_height + 50
    elif edge in ['left_t', 'right_t']:
        initial_x = -50 if edge == 'left_t' else const.screen_width + 50
        initial_y = random.randint(int(0.05 * const.screen_height), int(0.45 * const.screen_height))
    elif edge in ['left_b', 'right_b']:
        initial_x = -50 if edge == 'left_b' else const.screen_width + 50
        initial_y = random.randint(int(0.55 * const.screen_height), int(0.95 * const.screen_height))

    angle = radians(random.uniform(min_angle, max_angle))
    speed = random.uniform(const.MIN_SPEED_FLYING_OBJECT, const.MAX_SPEED_FLYING_OBJECT)
    velocity = [speed * cos(angle), -speed * sin(angle)]
    # randomize a flying object
    # use x-velocity to determine which pic to use
    if velocity[0] < 0:
        return FlyingObject(initial_x, initial_y, random.choice(flying_objects)[0], velocity, speed)
    else:
        return FlyingObject(initial_x, initial_y, random.choice(flying_objects)[1], velocity, speed)


#spawn new plane that flies on a static path across the screen.
def spawn_plane():
    dir = random.randint(0,1)
    speed = random.uniform(const.MIN_SPEED_PLANE, const.MAX_SPEED_PLANE)
    if dir == 0:
        angle = radians(195)
        plane = plane_l
        start_x = const.screen_width+50
        start_y = random.randint(int(0.10 * const.screen_height), int(0.60 * const.screen_height))
    elif dir == 1:
        angle = radians(345)
        plane = plane_r
        start_x = -(game_setup.PLANE_R_WIDTH)
        start_y = random.randint(int(0.10 * const.screen_height), int(0.60 * const.screen_height))
    velocity = [speed * cos(angle), -speed * sin(angle)] 
    return FlyingObject(start_x, start_y, plane, velocity, speed)

def spawn_time_adder():
    start_x = random.randint(int(0.15 * const.screen_width), int(0.85 * const.screen_width))
    start_y = random.randint(int(0.15 * const.screen_height), int(0.85 * const.screen_height))
    return TimedObject(x=start_x, y=start_y, image=game_setup.BONUS_TIME_CLOCK, lifespan=3, start_size_modifier=0.1, max_size_modifier=0.3, growth_rate=0.1)