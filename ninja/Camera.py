class Camera():
	def __init__(self, screen_size):
		self.x = screen_size[0]/2
		self.y = screen_size[1]/2
		self.screen_size = screen_size
		self.bounds = (0, 0)
	def set_focus(self, (x, y), ignore_bounds=False):
		objetivoX = x-self.screen_size[0]/2
		objetivoY = y-self.screen_size[1]/2
		if self.x!=objetivoX:
			dif = objetivoX-self.x
			self.x += dif/10
		if self.y!=objetivoY:
			dif = objetivoY-self.y+100
			self.y += dif/10
		if not ignore_bounds:
			self.check_sides()
	def check_sides(self):
		pass
#		if self.x<0:
#			self.x = 0
#		elif self.x>self.bounds[0]:
#			self.x = self.bounds[0]
#		if self.y<0:
#			self.y = 0
#		elif self.y>self.bounds[1]:
#			self.y = self.bounds[1]
	def change_screen_size(screen_size):
		self.screen_size = screen_size
		self.x = screen_size[0]/2
		self.y = screen_size[1]/2