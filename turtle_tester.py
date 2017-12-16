# -*- coding: utf-8 -*-
import math

_all_turtles = []


class Vec2D(tuple):
    """A 2 dimensional vector class, used as a helper class
    for implementing turtle graphics.
    May be useful for turtle graphics programs also.
    Derived from tuple, so a vector is a tuple!

    Provides (for a, b vectors, k number):
       a+b vector addition
       a-b vector subtraction
       a*b inner product
       k*a and a*k multiplication with scalar
       |a| absolute value of a
       a.rotate(angle) rotation
    """

    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    def __add__(self, other):
        return Vec2D(self[0] + other[0], self[1] + other[1])

    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return self[0] * other[0] + self[1] * other[1]
        return Vec2D(self[0] * other, self[1] * other)

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec2D(self[0] * other, self[1] * other)

    def __sub__(self, other):
        return Vec2D(self[0] - other[0], self[1] - other[1])

    def __neg__(self):
        return Vec2D(-self[0], -self[1])

    def __abs__(self):
        return (self[0] ** 2 + self[1] ** 2) ** 0.5

    def rotate(self, angle):
        """rotate self counterclockwise by angle
        """
        perp = Vec2D(-self[1], self[0])
        angle = angle * math.pi / 180.0
        c, s = math.cos(angle), math.sin(angle)
        return Vec2D(self[0] * c + perp[0] * s, self[1] * c + perp[1] * s)

    def __getnewargs__(self):
        return (self[0], self[1])

    def __repr__(self):
        return "({:+7.2f}, {:+7.2f})".format(*self)


class Screen:
    def __init__(self):
        pass

    def window_width(self):
        return 1000

    def window_height(self):
        return 1000

    def tracer(self, n):
        pass


class Turtle:
    def __init__(self, coords=Vec2D(0, 0), heading=0, pendown=True):
        self._coords = coords
        self._heading = heading
        self._pendown = pendown
        _all_turtles.append(self)

    def clone(self):
        return Turtle(self._coords, self._heading, self._pendown)

    def forward(self, distance):
        new_coords = self._coords + Vec2D(math.cos(self._heading), math.sin(self._heading)) * distance
        if self._pendown:
            print(self._coords, '->', new_coords)
        self._coords = new_coords

    def backward(self, distance):
        new_coords = self._coords - Vec2D(math.cos(self._heading), math.sin(self._heading)) * distance
        if self._pendown:
            print(self._coords, '->', new_coords)
        self._coords = new_coords

    def right(self, angle):
        self._heading -= angle / 180 * math.pi

    def left(self, angle):
        self._heading += angle / 180 * math.pi

    def pendown(self):
        self._pendown = True

    def penup(self):
        self._pendown = False

    def goto(self, x, y):
        new_coords = Vec2D(x, y)
        if self._pendown:
            print(self._coords, '->', new_coords)
        self._coords = new_coords

    def home(self):
        new_coords = Vec2D(0, 0)
        if self._pendown:
            print(self._coords, '->', new_coords)
        self._coords = new_coords
        self._heading = 0

    def setx(self, x):
        new_coords = Vec2D(x, self._coords[1])
        if self._pendown:
            print(self._coords, '->', new_coords)
        self._coords = new_coords

    def sety(self, y):
        new_coords = Vec2D(self._coords[0], y)
        if self._pendown:
            print(self._coords, '->', new_coords)
        self._coords = new_coords

    def setheading(self, to_angle):
        self._heading = to_angle / 180 * math.pi

    def pensize(self):
        pass

    def pencolor(self):
        pass

    def fillcolor(self):
        pass

    def begin_fill(self):
        pass

    def end_fill(self):
        pass

    def showturtle(self):
        pass

    def hideturtle(self):
        pass

    def write(self):
        pass

    def speed(self):
        pass

    def getscreen(self):
        return Screen()

    def position(self):
        return tuple(self._coords)

    def xcor(self):
        return self._coords[0]

    def ycor(self):
        return self._coords[0]

    def heading(self):
        return self._heading * 180 / math.pi

    def distance(self, x, y):
        return math.hypot(x - self._coords[0], y - self._coords[1])

    def isdown(self):
        return self._pendown


def onkey(*args, **kwargs):
    pass


def listen(*args, **kwargs):
    pass


def ontimer(*args, **kwargs):
    pass


def mainloop(*args, **kwargs):
    pass


def textinput(*args, **kwargs):
    return input()


def setworldcoordinates(*args, **kwargs):
    pass


_default_turtle = Turtle()

for name in dir(_default_turtle):
    if not name.startswith('_'):
        code = '{name} = _default_turtle.{name}'.format(name=name)
        exec(code)


def turtles():
    return _all_turtles.copy()
