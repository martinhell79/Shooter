import game_setup
import pygame
import constants as const


name_rect_x = const.screen_width * 0.03
name_rect_y = const.screen_height * 0.4
name_rect_width = const.screen_width * 0.2
name_rect_height = 40
name_rect = pygame.Rect(name_rect_x,name_rect_y, name_rect_width, name_rect_height)

email_rect_x = const.screen_width * 0.03
email_rect_y = const.screen_height * 0.50
email_rect_width = const.screen_width * 0.2
email_rect_height = 40
email_rect = pygame.Rect(email_rect_x,email_rect_y,email_rect_width,email_rect_height)

# position for clear images. x-pos will be updated when rendered since width might change.
clear_name_x = name_rect.x - 55
clear_name_y = name_rect.y + 1

clear_email_x = email_rect.x - 55
clear_email_y = email_rect.y + 1

# Keep track of which entry is active
name_rect_active = True
email_rect_active = False


start_img_x = const.screen_width - game_setup.start_img.get_width() - 70
start_img_y = const.screen_height - game_setup.start_img.get_height() - 50


def eraseActiveString():
    if name_rect_active:
       game_setup.user_name = game_setup.user_name[:-1]
    elif email_rect_active:
        game_setup.user_email = game_setup.user_email[:-1] 

def appendActiveString(c):
    if name_rect_active and len(game_setup.user_name) < 12:
       game_setup.user_name += c
    elif email_rect_active and len(game_setup.user_email) < 45:
        game_setup.user_email += c

def switchActiveBox(str=''):
    global name_rect_active, email_rect_active
    if str == 'name' or (str == '' and email_rect_active):
        name_rect_active = True
        email_rect_active = False
    elif str == 'email' or (str == '' and name_rect_active):
        name_rect_active = False
        email_rect_active = True

