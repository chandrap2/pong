import pygame as pyg
import game_constants as g_const
from TextBox import TextBox

class Player():
	
	# input: display Surface object, boolean to determine which side of field
	def __init__(self, left):
		# uses screen dimensions for player placement
		self.screen_dim = g_const.screen_dim
		
		# player dimensions
		self.p_w = g_const.p_w
		self.p_h = g_const.p_h
		
		# surface to be displayed, rect to be transformed
		self.p_surface = g_const.face_surface
		self.p_surface = pyg.transform.scale(self.p_surface, (self.p_w, self.p_h))
		self.p_rect = self.p_surface.get_rect() # pos: 0, 0
		
		self.p_speed = g_const.p_speed
		
		self.p_left = left
		if not left:
			self.p_rect.x = self.screen_dim.w - self.p_rect.w
		
		self.score = 0
		self.show_winner_text = False
		self.pause_for_win = False
		
		self.score_text = TextBox(40, g_const.game_text_font, g_const.game_text_color, self.p_left)
		self.win_text = TextBox(20, g_const.game_text_font, g_const.game_text_color, self.p_left)
		
		if self.p_left:
			self.score_text.set_pos(self.screen_dim.w // 2, self.screen_dim.h - 50)
			self.score_text.set_right_align(self.screen_dim.w // 2 - 15)
			
			self.win_text.set_pos(self.screen_dim.w // 2, self.screen_dim.h // 2 + 40)
			self.win_text.set_right_align(self.screen_dim.w // 2 - 15)
		else:
			self.score_text.set_pos(self.screen_dim.w // 2 + 15, self.screen_dim.h - 50)
			self.win_text.set_pos(self.screen_dim.w // 2 + 15, self.screen_dim.h // 2 + 40)
		self.win_text.update_text("WINNER")
		
		self.up_state = self.down_state = False
		
		self.reset_player()
	
	def update(self, events):
		self.player_event_listener(events)
		
		if self.up_state:
			self.p_rect.move_ip((0, -self.p_speed if self.p_rect.top >= 0 else 0))
		if self.down_state:
			self.p_rect.move_ip((0, self.p_speed if self.p_rect.bottom < self.screen_dim.h else 0))
		
		if self.score == g_const.winning_score and not self.pause_for_win:
			pyg.event.post(self.create_game_won_ev(g_const.p_p1_won_id if self.p_left else g_const.p_p2_won_id))
			self.show_winner_text = True
	
	def player_event_listener(self, events):
		for event in events:
			if event.type == pyg.KEYDOWN:
				if self.p_left:
					if event.key == pyg.K_w:
						self.up_state = True
					elif event.key == pyg.K_s:
						self.down_state = True
				else:
					if event.key == pyg.K_UP:
						self.up_state = True
					elif event.key == pyg.K_DOWN:
						self.down_state = True
				
				if self.pause_for_win and event.key == pyg.K_SPACE:
					self.pause_for_win = False
					self.show_winner_text = False
					
					self.reset_score()
					self.score_text.update_text(str(self.score))
			
			elif event.type == pyg.KEYUP:
				if self.p_left:
					if event.key == pyg.K_w:
						self.up_state = False
					elif event.key == pyg.K_s:
						self.down_state = False
				else:
					if event.key == pyg.K_UP:
						self.up_state = False
					elif event.key == pyg.K_DOWN:
						self.down_state = False
			
			elif event.type == g_const.GAMEREADY_ID:
				if event.move_to_player_id != 0:
					if event.move_to_player_id == 1:
						if self.p_left: self.score += 1
					else:
						if not self.p_left: self.score += 1
				
				self.score_text.update_text(str(self.score))
			elif event.type == g_const.GAMEWIN_ID:
				self.pause_for_win = True
	
	def get_pos(self):
		pos = (self.p_rect.x, self.p_rect.y)
		return pos
	
	# center player position
	def reset_player(self):
		self.p_rect.centery = self.screen_dim.h // 2
	
	def reset_score(self):
		self.score = 0
	
	def create_game_won_ev(self, player_won_id):
		event = g_const.GAMEWIN_EV
		event.winning_player_id = player_won_id
		return event
