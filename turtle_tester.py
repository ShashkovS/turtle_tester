# -*- coding: utf-8 -*-
import math

__all__ = ['ScrolledCanvas', 'TurtleScreen', 'Screen', 'RawTurtle', 'Turtle', 'RawPen', 'Pen', 'Shape', 'Vec2D', 'back',
           'backward', 'begin_fill', 'begin_poly', 'bk', 'addshape', 'bgcolor', 'bgpic', 'bye', 'clearscreen',
           'colormode', 'delay', 'exitonclick', 'getcanvas', 'getshapes', 'listen', 'mainloop', 'mode', 'numinput',
           'onkey', 'onkeypress', 'onkeyrelease', 'onscreenclick', 'ontimer', 'register_shape', 'resetscreen',
           'screensize', 'setup', 'Terminator', 'setworldcoordinates', 'textinput', 'title', 'tracer', 'turtles',
           'update', 'window_height', 'window_width', 'write_docstringdict', 'done', 'circle', 'clear', 'clearstamp',
           'clearstamps', 'clone', 'color', 'degrees', 'distance', 'dot', 'down', 'end_fill', 'end_poly', 'fd',
           'fillcolor', 'filling', 'forward', 'get_poly', 'getpen', 'getscreen', 'get_shapepoly', 'getturtle', 'goto',
           'heading', 'hideturtle', 'home', 'ht', 'isdown', 'isvisible', 'left', 'lt', 'onclick', 'ondrag', 'onrelease',
           'pd', 'pen', 'pencolor', 'pendown', 'pensize', 'penup', 'pos', 'position', 'pu', 'radians', 'right', 'reset',
           'resizemode', 'rt', 'seth', 'setheading', 'setpos', 'setposition', 'settiltangle', 'setundobuffer', 'setx',
           'sety', 'shape', 'shapesize', 'shapetransform', 'shearfactor', 'showturtle', 'speed', 'st', 'stamp', 'tilt',
           'tiltangle', 'towards', 'turtlesize', 'undo', 'undobufferentries', 'up', 'width', 'write', 'xcor', 'ycor']


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
        return tuple.__new__(cls, (float(x), float(y)))

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
        return "({},{})".format(*self)


class Screen:
    def __init__(self):
        pass

    def window_width(self):
        return 1000

    def window_height(self):
        return 1000

    def tracer(self, *args, **kwargs):
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
            print(self._coords, '->', new_coords, sep='')
        self._coords = new_coords

    def backward(self, distance):
        new_coords = self._coords - Vec2D(math.cos(self._heading), math.sin(self._heading)) * distance
        if self._pendown:
            print(self._coords, '->', new_coords, sep='')
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
            print(self._coords, '->', new_coords, sep='')
        self._coords = new_coords

    def home(self):
        new_coords = Vec2D(0, 0)
        if self._pendown:
            print(self._coords, '->', new_coords, sep='')
        self._coords = new_coords
        self._heading = 0

    def setx(self, x):
        new_coords = Vec2D(x, self._coords[1])
        if self._pendown:
            print(self._coords, '->', new_coords, sep='')
        self._coords = new_coords

    def sety(self, y):
        new_coords = Vec2D(self._coords[0], y)
        if self._pendown:
            print(self._coords, '->', new_coords, sep='')
        self._coords = new_coords

    def setheading(self, to_angle):
        self._heading = to_angle / 180 * math.pi

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

    fd = forward
    bk = backward
    back = backward
    rt = right
    lt = left
    pos = position
    setpos = goto
    setposition = goto
    seth = setheading


def _dummy_func(*args, **kwargs):
    pass


_default_turtle = Turtle()

for name in dir(_default_turtle):
    if not name.startswith('_'):
        code = '{name} = _default_turtle.{name}'.format(name=name)
        exec(code)


def turtles():
    return _all_turtles.copy()


cur_dir = set(dir())
turtle_functions = ['Screen', 'addshape', 'back', 'backward', 'begin_fill', 'begin_poly', 'bgcolor', 'bgpic', 'bk',
                    'bye', 'circle', 'clear', 'clearscreen', 'clearstamp', 'clearstamps', 'clone', 'color', 'colormode',
                    'config_dict', 'deepcopy', 'degrees', 'delay', 'distance', 'done', 'dot', 'down', 'end_fill',
                    'end_poly', 'exitonclick', 'fd', 'fillcolor', 'filling', 'forward', 'get_poly', 'get_shapepoly',
                    'getcanvas', 'getmethparlist', 'getpen', 'getscreen', 'getshapes', 'getturtle', 'goto', 'heading',
                    'hideturtle', 'home', 'ht', 'isdown', 'isfile', 'isvisible', 'join', 'left', 'listen', 'lt',
                    'mainloop', 'mode', 'numinput', 'onclick', 'ondrag', 'onkey', 'onkeypress', 'onkeyrelease',
                    'onrelease', 'onscreenclick', 'ontimer', 'pd', 'pen', 'pencolor', 'pendown', 'pensize', 'penup',
                    'pos', 'position', 'pu', 'radians', 'read_docstrings', 'readconfig', 'register_shape', 'reset',
                    'resetscreen', 'resizemode', 'right', 'rt', 'screensize', 'seth', 'setheading', 'setpos',
                    'setposition', 'settiltangle', 'setundobuffer', 'setup', 'setworldcoordinates', 'setx', 'sety',
                    'shape', 'shapesize', 'shapetransform', 'shearfactor', 'showturtle', 'speed', 'split', 'st',
                    'stamp',
                    'textinput', 'tilt', 'tiltangle', 'title', 'towards', 'tracer', 'turtles', 'turtlesize', 'undo',
                    'undobufferentries', 'up', 'update', 'width', 'window_height', 'window_width', 'write',
                    'write_docstringdict', 'xcor', 'ycor']
for name in turtle_functions:
    if name not in cur_dir:
        code = '{name} = _dummy_func'.format(name=name)
        exec(code)

turtle_methods = ['back', 'backward', 'begin_fill', 'begin_poly', 'bk', 'circle', 'clear', 'clearstamp', 'clearstamps',
                  'clone', 'color', 'degrees', 'distance', 'dot', 'down', 'end_fill', 'end_poly', 'fd', 'fillcolor',
                  'filling', 'forward', 'get_poly', 'get_shapepoly', 'getpen', 'getscreen', 'getturtle', 'goto',
                  'heading', 'hideturtle', 'home', 'ht', 'isdown', 'isvisible', 'left', 'lt', 'onclick', 'ondrag',
                  'onrelease', 'pd', 'pen', 'pencolor', 'pendown', 'pensize', 'penup', 'pos', 'position', 'pu',
                  'radians', 'reset', 'resizemode', 'right', 'rt', 'seth', 'setheading', 'setpos', 'setposition',
                  'settiltangle', 'setundobuffer', 'setx', 'sety', 'shape', 'shapesize', 'shapetransform',
                  'shearfactor', 'showturtle', 'speed', 'st', 'stamp', 'tilt', 'tiltangle', 'towards', 'turtlesize',
                  'undo', 'undobufferentries', 'up', 'width', 'write', 'xcor', 'ycor', ]
turtle_dir = set(dir(_default_turtle))
for name in turtle_methods:
    if name not in turtle_dir:
        code = 'setattr(Turtle, "{name}", _dummy_func)'.format(name=name)
        exec(code)


class Pen:
    pass
class RawPen:
    pass
class RawTurtle(Turtle):
    pass
class ScrolledCanvas:
    pass
class Shape:
    pass
class Terminator:
    pass
class TurtleScreen(Screen):
    pass
