"""
Implementation of 2d geometry and mathematics
compatible with both Python2 and Python3
To be used as:

>>> from PyParticles.Maths import *
>>> v = Vector(3,4)
"""
from __future__ import print_function, division
import math


class Vector(object):
    """
    A vector class to be used for all the physical calculations
    default Type: Cartesian (xI + yJ)
    >>> v1 = Vector(3,4) # 3I + 4J
    >>> v2 = Vector(2,0.5,polar=True) # r=2, theta=0.5
    """

    def __init__(self, r_x, t_y, polar=False):
        self._r = 0
        self._t = 0
        self.x = 0
        self.y = 0

        if polar:
            self._r = r_x
            self._t = t_y
            self._polar_to_car()
        else:
            self.x = r_x
            self.y = t_y

    def _polar_to_car(self):
        self.x = self._r * math.cos(self._t)
        self.y = self._r * math.sin(self._t)

    def _car_to_polar(self):
        self._r = math.hypot(self.x, self.y)
        self._t = 0.5 * math.pi - math.atan2(self.y, self.x)

    def __add__(self, vec):
        if not isinstance(vec, Vector):
            raise TypeError("Vector addition should be with vectors")
        else:
            ret_x = self.x + vec.x
            ret_y = self.y + vec.y
            return Vector(ret_x, ret_y)

    def __sub__(self, vec):
        return self.__add__(vec * (-1))

    def __mul__(self, v):
        try:
            supp_types = (int, float, long)
        except NameError:
            supp_types = (int, float)
        if isinstance(v, supp_types):
            return Vector(self.x * v, self.y * v)
        elif isinstance(v, Vector):
            return self.x * v.x + self.y * v.y

    def __pow__(self, v):
        """
        This is used to evaluate the cross product of two vectors
        vec1 ** vec2 => cross product of vec1 and vec2
        here since cross product has ony one direction in 2d geometry
        we would consider only the magnitude of cross product
        """
        if isinstance(v, Vector):
            return self.r * v.r * math.sin(abs(self.t - v.t))
        else:
            raise TypeError("Cross product should be done with vectors only")

    def __eq__(self, vec):
        if isinstance(vec, Vector):
            return (self.x == vec.x) and (self.y == vec.y)
        else:
            raise TypeError

    def __str__(self):
        return str(self.x) + 'i + ' + str(self.y) + 'j\n(' + str(self.r) + ', ' + str(self.t) + ')'

    def __getattr__(self, item):
        if item == 'car':
            return self.x, self.y

        elif item == 'polar':
            return self.r, self.t

        elif item == 'r':
            self._car_to_polar()
            return self._r

        elif item == 't':
            self._car_to_polar()
            return self._t

        else:
            raise ValueError('Value can be either p: polar or c: cartesian')


def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


if __name__ == '__main__':
    v = Vector(3, 4)
    print(v)
    print(v.polar)
