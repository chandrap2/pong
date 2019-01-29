import pygame as pyg
pyg.init()

class TextBox():
	# input: display Surface object
	def __init__(self, text_size, text_font, text_color, is_right_align):
		self.text_size = text_size
		self.text_font = text_font
		self.text_color = text_color
		self.is_right_align = is_right_align
		self.right_align = 0
		
		# surface to be displayed, rect to be transformed
		self.text_font = pyg.font.SysFont(text_font, text_size)
		self.t_surface = self.text_font.render("", True, text_color)
		self.t_rect = self.t_surface.get_rect() # pos: 0, 0
	
	def set_pos(self, x, y):
		self.t_rect.x = x # dummy x if right-aligned
		self.t_rect.y = y
	
	def get_pos(self):
		pos = (self.t_rect.x, self.t_rect.y)
		return pos
	
	# sets x value to align right side of bounding rect to
	def set_right_align(self, x):
		self.right_align = x
	
	# updates surface with new text, bounding rect (also position if right-aliged)
	def update_text(self, text):
		self.t_surface = self.text_font.render(text, True, self.text_color) # doesn't draw anything, just returns a surface
		self.t_rect.size = self.t_surface.get_rect().size
		
		if self.is_right_align:
			self.t_rect.right = self.right_align
