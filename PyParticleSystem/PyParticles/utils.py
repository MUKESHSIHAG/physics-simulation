import math

def add_vectors(vector1, vector2):
	#Note the vectors are tuple (angle, magnitude)
	x = math.sin(vector1[0]) * vector1[1] + math.sin(vector2[0]) * vector2[1]
	y = math.cos(vector1[0]) * vector1[1] + math.cos(vector2[0]) * vector2[1]
	mag = math.hypot(x, y)
	angle = (math.pi/2) - math.atan2(y, x)
	return (angle, mag)
