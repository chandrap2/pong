import sys, time, pygame as pyg
import game_constants as g_const

from random import randint
from Player import Player
from Ball import Ball
from TextBox import TextBox

pyg.init() # initialize modules
# pyg.event.set_blocked([pyg.MOUSEMOTION, pyg.MOUSEBUTTONUP, pyg.MOUSEBUTTONDOWN, pyg.KEYUP, pyg.KEYDOWN]) # blocking unwanted events
pyg.event.set_allowed([pyg.KEYUP, pyg.KEYDOWN, g_const.GAMEREADY_ID]) # blocking unwanted events

fps = g_const.fps # desired framerate
frame_length = g_const.frame_length # in seconds

screen = g_const.screen
screen_dim = g_const.screen_dim

game_text_font = g_const.game_text_font
game_text_color = g_const.game_text_color

p1 = Player(True)
p2 = Player(False)
ball = Ball()

def main():
	start = time.time()
	
	while 1:
		dt = time.time() - start
		
		if dt >= frame_length:
			# if 1 / dt < 58: print(1 / dt)
			start = time.time() # reset start tick
			
			# handle events
			events = pyg.event.get()
			for event in events:
				if event.type == pyg.QUIT:
					sys.exit()
			
			dt += time.time() - start
			p1.update(events, dt)
			p2.update(events, dt)
			ball.update(p1, p2, events)
			
			# draw background and objects
			screen.fill((0, 0, 0))
			pyg.draw.line(screen, game_text_color, (screen_dim.w // 2, 0), (screen_dim.w // 2, screen_dim.h), 3)
			
			screen.blit(p1.score_text.t_surface, p1.score_text.get_pos()) # will be right-aligned
			screen.blit(p2.score_text.t_surface, p2.score_text.get_pos())
			
			if p1.show_winner_text:
				# print(p1.pause_for_win, p2.pause_for_win)
				screen.blit(p1.win_text.t_surface, p1.win_text.get_pos())
			elif p2.show_winner_text:
				# print(p1.pause_for_win, p2.pause_for_win)
				screen.blit(p2.win_text.t_surface, p2.win_text.get_pos())
			
			screen.blit(ball.b_surface, ball.b_rect)
			screen.blit(p1.p_surface, p1.p_rect)
			screen.blit(p2.p_surface, p2.p_rect)
			
			# update display
			pyg.display.update()

def is_button_pressed(int_id): # return whether specified key was pressed at that moment
	pressed = pyg.key.get_pressed()[int_id]
	return pressed

main()
