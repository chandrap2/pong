import pygame as pyg

GAMEREADY_ID = pyg.USEREVENT
GAMEREADY_EV = pyg.event.Event(GAMEREADY_ID, move_to_player_id = 1)
