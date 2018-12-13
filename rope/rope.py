from time import sleep
from graphics import *
from math import sqrt
from random import randint
win = GraphWin("Rope Physics", 800, 800)

CONST_GRAV = 0.05

def map(x, in_min, in_max, out_min, out_max):
  return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def getDir(old, new):
	if old > new:
		return 1
	if old < new:
		return -1
	return 1

class RopeElement():
	def __init__(self, x, y, c1, c2, fixed, objects, w, color):
		self.x = x
		self.y = y
		self.sX = 0
		self.sY = 0
		self.f = c1
		self.b = c2
		self.prev = None
		self.fix = fixed
		self.o = objects
		self.w = w
		self.color = color
		
	def sim(self, coll, index):
		if not self.fix:
			if not coll:
				self.mov()
			else:
				self.sY = self.sY + self.w
				if self.y > 798:
					self.y = 798
					self.sY = self.sY * -0.3
				if self.f != None and sqrt(pow(abs(self.x - self.f.x), 2) + pow(abs(self.y - self.f.y), 2)) > 4:
					#self.x = self.x - self.sX
					#self.y = self.y - self.sY
					newX = (((self.f.x - self.x) / 7) + self.sX)
					newY = (((self.f.y - self.y) / 7) + self.sY)
					self.sX = newX
					self.sY = newY
				if self.b != None and sqrt(pow(abs(self.x - self.b.x), 2) + pow(abs(self.y - self.b.y), 2)) > 4:
					#self.x = self.x - self.sX
					#self.y = self.y - self.sY
					newX = (((self.b.x - self.x) / 7) + self.sX)
					newY = (((self.b.y - self.y) / 7) + self.sY)
					self.sX = newX
					self.sY = newY
				for i in range(len(objects)):
					if self.x < objects[i].x + objects[i].w and self.x > objects[i].x - objects[i].w and self.y < objects[i].y + objects[i].w and self.y > objects[i].y - objects[i].w:
						self.sX = (self.x - objects[i].x) / (objects[i].w / 2)
						self.sY = (self.y - objects[i].y) / (objects[i].w / 2)
			if index == 0:
				pt = win.checkMouse()
				if pt != None:
					newX = (((int(pt.getX()) - self.x) / 50) + self.sX)
					newY = (((int(pt.getY()) - self.y) / 50) + self.sY)
					self.sX = newX
					self.sY = newY

	def mov(self):
		self.x = self.x + self.sX
		self.y = self.y + self.sY
					
	def draw(self, i, max, preview):
		if self.prev != None:
			self.prev.undraw()
		if preview:
			l = Circle(Point(self.x, self.y), 4)
			l.setFill(self.color)
			l.draw(win)
			self.prev = l
		elif i != max:
			l = Line(Point(self.x, self.y), Point(self.b.x, self.b.y))
			l.setFill(self.color)
			l.setWidth(6)
			l.draw(win)
			self.prev = l

	def setConn(self, c1, c2):
		self.f = c1
		self.b = c2

	def setFixed(self, fixed):
		self.fix = fixed

	def setWeight(self, w):
		self.w = w

class Object:
	def __init__(self, x, y, w, id):
		self.x = x
		self.y = y
		self.w = w
		self.p = None
		self.t = None
		self.id = id

	def draw(self):
		c = Circle(Point(self.x, self.y), self.w)
		c.setFill('red')
		c.draw(win)
		i = Text(Point(self.x, self.y), str(self.id))
		i.draw(win)
		self.t = i
		self.p = c

	def undraw(self):
		self.p.undraw()
		self.t.undraw()

	def getId(self):
		return self.id
		
rope = []
ELEMENTS = 40

objects = []

#b = Object(325, 500, 40)
#b.draw()
#objects.append(b)

#b = Object(425, 500, 40)
#b.draw()
#objects.append(b)

#b = Object(375, 600, 40)
#b.draw()
#objects.append(b)


b = Object(300, 300, 40, 1) # These two are important!
b.draw()
objects.append(b)

b = Object(500, 300, 40, 2)
b.draw()
objects.append(b)

while win.checkKey() != 'd':
	pt = win.checkMouse()
	if pt != None:
		newX = int(pt.getX())
		newY = int(pt.getY())
		try:
			prevX = rope[len(rope) - 1].x
			prevY = rope[len(rope) - 1].y
			if abs(prevX - newX) > abs(prevY - newY):
				max_val = max(prevX, newX)
				min_val = min(prevX, newX)
			else:
				max_val = max(prevY, newY)
				min_val = min(prevY, newY)
			for i in range(min_val, max_val, 8):
				newRope = RopeElement(map(i, min_val, max_val, prevX, newX), map(i, min_val, max_val, prevY, newY), None, None, False, objects, 0.05, color_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
				newRope.draw(len(rope) - 1, len(rope) - 1, 1)
				rope.append(newRope)
		except Exception as e:
			newRope = RopeElement(newX, newY, None, None, False, objects, 0.05, color_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
			newRope.draw(len(rope) - 1, len(rope) - 1, 1)
			rope.append(newRope)
#for i in range(ELEMENTS):
#        newRope = RopeElement(400 - (ELEMENTS - i) * 8, 90, None, None, False, objects)
#        rope.append(newRope)

for i in range(len(rope)):
	if i == 0:
		rope[i].setConn(None, rope[i + 1])
		#rope[i].setWeight(5)
	elif i == len(rope) - 1:
		rope[i].setConn(rope[i - 1], None)
		#rope[i].setWeight(5)
	else:
		rope[i].setConn(rope[i - 1], rope[i + 1])

#rope[len(rope) - 1].setFixed(True) # End fixed
#rope[int(len(rope) / 2)].setFixed(True) # Middle fixed

def deleteO(id, objects):
	for i in range(len(objects)):
		if objects[i].getId() == id:
			objects[i].undraw()
			del objects[i]
			return

while True:
	for i in range(len(rope)):
		rope[i].sim(0, i)
	for i in range(len(rope)):
		rope[i].sim(1, i)
		rope[i].draw(i, len(rope) - 1, 0)
	key = win.checkKey()
	if key == '1':
		deleteO(1, objects)
	if key == '2':
		deleteO(2, objects)
	#sleep(0.01)
