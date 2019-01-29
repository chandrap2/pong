import pygame as pyg

# general game constants
fps = 20 # desired framerate
frame_length = 1.0 / fps # in seconds

screen_size = w, h = 320, 240
screen = pyg.display.set_mode(screen_size)
screen_dim = screen.get_rect()

face_surface = pyg.image.load("face.png").convert()

game_text_font = pyg.font.get_default_font()
game_text_color = pyg.Color(100, 100, 100)

winning_score = 5

""" player constants """
p_w = 17
p_h = 75
p_speed = 5 # pixels/frame
# p_speed = 5 * fps = 300 # pixels/sec

p_p1_won_id = 1
p_p2_won_id = 2

""" ball constants """
b_w = 13
b_h = 13

# stationary collision objects at top and bottom of screen
top_rect = pyg.Rect(0, -5, screen_dim.w, 5)
bottom_rect = pyg.Rect(0, screen_dim.h, screen_dim.w, 5)
collide_rects = [top_rect, bottom_rect]

b_vel_mag = 9 # pixels/frame
# b_vel_mag = 9 * fps = 540 # pixels/sec
b_angle_range = 60 # max angle between normal of player collided against and vel of ball

b_player_coll_top_id = 1
b_player_coll_side_id = 2
b_player_coll_bottom_id = 3

b_move_to_rand_p_id = 0
b_move_to_p_1_id = 1
b_move_to_p_2_id = 2

# events
GAMEREADY_ID = pyg.USEREVENT
GAMEREADY_EV = pyg.event.Event(GAMEREADY_ID, move_to_player_id = b_move_to_rand_p_id)

GAMEWIN_ID = pyg.USEREVENT + 1
GAMEWIN_EV = pyg.event.Event(GAMEWIN_ID, winning_player_id = p_p1_won_id)
