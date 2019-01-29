import pygame as pyg
import game_constants as g_const
from random import randint
from math import sin, cos, pi

class Ball():
	
	# input: display Surface object
	def __init__(self):
		# uses screen dimensions for player placement
		self.screen_dim = g_const.screen_dim
		
		# ball dimensions
		self.b_w = g_const.b_w
		self.b_h = g_const.b_h
		
		# surface to be displayed, rect to be transformed
		self.b_surface = g_const.face_surface
		self.b_surface = pyg.transform.scale(self.b_surface, (self.b_w, self.b_h))
		self.b_rect = self.b_surface.get_rect() # pos: 0, 0
		
		self.collide_rects = g_const.collide_rects
		
		self.vel_mag = g_const.b_vel_mag
		self.angle_range = g_const.b_angle_range
		
		self.b_velx = self.b_vely = 0
		self.ball_game_state = False
		
		self.PLAYER_COLL_TOP = g_const.b_player_coll_top_id
		self.PLAYER_COLL_SIDE = g_const.b_player_coll_side_id
		self.PLAYER_COLL_BOTTOM = g_const.b_player_coll_bottom_id
		
		self.MOVE_TO_RAND_P = g_const.b_move_to_rand_p_id
		self.MOVE_TO_P_1 = g_const.b_move_to_p_1_id
		self.MOVE_TO_P_2 = g_const.b_move_to_p_2_id
		
		event = self.create_restart_game_ev(self.MOVE_TO_RAND_P)
		pyg.event.post(event)
	
	def update(self, p1, p2, events):
		self.ball_event_listener(events)
		
		if self.ball_game_state: # game is ongoing
			self.b_rect.move_ip(self.b_velx, self.b_vely)
			
			# post restart_game event if ball is completely out of bounds
			if self.b_rect.right < 0 or self.b_rect.left > self.screen_dim.w:
				if self.b_rect.right < 0: # player 1 loses match
					event = self.create_restart_game_ev(self.MOVE_TO_P_2)
				else: # player 2 loses match
					event = self.create_restart_game_ev(self.MOVE_TO_P_1)
				pyg.event.post(event)
				return
			
			# collision with players
			if self.b_rect.colliderect(p1.p_rect): self.react_to_player_coll(p1)
			elif self.b_rect.colliderect(p2.p_rect): self.react_to_player_coll(p2)
			
			# checking for collisions with top or bottom of screen
			first_coll_index = self.b_rect.collidelist(self.collide_rects)
			if first_coll_index == 0 or first_coll_index == 1:
				self.b_vely *= -1
				
				if first_coll_index == 0: # top
					self.b_rect.top = 0
				else: # bottom
					self.b_rect.bottom = self.screen_dim.h
	
	def ball_event_listener(self, events):
		for event in events:
			if event.type == g_const.GAMEREADY_ID: # reset game
				self.ball_game_state = False
				self.reset_ball(event.move_to_player_id)
			elif event.type == g_const.GAMEWIN_ID:
				self.reset_vel(g_const.b_move_to_rand_p_id)
				continue
			
			if not self.ball_game_state:
				if event.type == pyg.KEYDOWN and event.key == pyg.K_SPACE: # start game if unpaused
					self.ball_game_state = True
	
	def get_pos(self):
		pos = (self.b_rect.x, self.b_rect.y)
		return pos
	
	def set_pos(self, x, y):
		self.b_rect.x = x
		self.b_rect.y = y
		# print(self.get_pos())
	
	# move ball to center of screen and reset velocities
	def reset_ball(self, player_id):
		self.reset_vel(player_id)
		screen_w = self.screen_dim.w
		screen_h = self.screen_dim.h
		self.set_pos(screen_w // 2, screen_h // 2 + randint(0, screen_h // 4))
	
	def reset_vel(self, player_id):
		random_angle = randint(0, 45)
		if player_id == g_const.b_move_to_rand_p_id: # ball will move towards bottom half of either player's half
			self.compute_vel_components(self.vel_mag, 225 * randint(0, 1) - random_angle)
		elif player_id == g_const.b_move_to_p_1_id: # ball will move towards bottom half of p1's half
			self.compute_vel_components(self.vel_mag, 180 + random_angle)
		else: # ball will move towards bottom half of p2's half
			self.compute_vel_components(self.vel_mag, -random_angle)
	
	# changes velocity of ball after collision with player
	# NOTE: call during frame of collision
	def react_to_player_coll(self, player):
		p_collide_side = self.compute_coll_edge(player)
		self.move_to_player_edge(player, p_collide_side)
		
		if p_collide_side == self.PLAYER_COLL_SIDE:
			angle = self.compute_reflect_angle(player, self.angle_range)
		else: # bounce out of bounds if ball hits top or bottom edge of player
			if player.p_left:
				if p_collide_side == self.PLAYER_COLL_TOP: angle = 120
				else: angle = 240
			else:
				if p_collide_side == self.PLAYER_COLL_TOP: angle = 60
				else: angle = -60
		
		self.compute_vel_components(self.vel_mag, angle)
	
	# return angle of reflectance based on location of collision with player's top or bottom collide rect
	def compute_reflect_angle(self, player, ang_range):
		ang_range = abs(ang_range)
		
		normalized = ang_range * (player.p_rect.centery - self.b_rect.centery) / ((player.p_rect.h + self.b_rect.h) / 2)
		result = normalized if player.p_left else 180 - normalized
		
		return result
	
	# sets velx and vely based on vel mag and angle in degrees
	def compute_vel_components(self, vel, angle):
		angle_rads = (angle / 180) * pi
		
		self.b_velx = int(vel * cos(angle_rads))
		self.b_vely = -int(vel * sin(angle_rads)) # larger y-values down the screen
	
	# returns which edge of the player the ball hits
	# NOTE: call during frame of collision; move_to_player_edge() WILL NEED to be called after this method's called
	def compute_coll_edge(self, player):
		# self.b_rect.move_ip(-self.b_velx, -self.b_vely)
		bound_slope = abs(self.b_vely / self.b_velx)
		
		if player.p_left:
			# y1 = y0 + m(x1 - x0)
			min_y = player.p_rect.top - bound_slope * (self.b_rect.left - player.p_rect.right)
			max_y = player.p_rect.bottom + bound_slope * (self.b_rect.left - player.p_rect.right)
		else:
			# y0 = y1 - m(x1 - x0)
			min_y = player.p_rect.top - bound_slope * (player.p_rect.left - self.b_rect.right)
			max_y = player.p_rect.bottom + bound_slope * (player.p_rect.left - self.b_rect.right)
		
		# bounds will be checked against center of ball
		min_y -= self.b_h / 2
		max_y += self.b_h / 2
		
		if self.b_rect.centery > max_y:
			return self.PLAYER_COLL_BOTTOM
		if self.b_rect.centery > min_y:
			return self.PLAYER_COLL_SIDE
		return self.PLAYER_COLL_TOP
	
	# moves ball to appropriate location on edge of player
	# NOTE: call during frame of collision after calling compute_coll_edge()
	def move_to_player_edge(self, player, location):
		slope = self.b_vely / self.b_velx
		
		if location == self.PLAYER_COLL_TOP or location == self.PLAYER_COLL_BOTTOM:
			if location == self.PLAYER_COLL_TOP:
				dy = player.p_rect.top - self.b_rect.bottom
			else:
				dy = player.p_rect.bottom - self.b_rect.top
			dx = dy / slope
		else: # hits side of player
			if player.p_left:
				dx = player.p_rect.right - self.b_rect.left
			else:
				dx = player.p_rect.left - self.b_rect.right
			dy = dx * slope
		
		# print(dx, dy)
		self.b_rect.move_ip(int(dx), int(dy))
	
	def create_restart_game_ev(self, player_id):
		event = g_const.GAMEREADY_EV
		event.move_to_player_id = player_id
		return event
