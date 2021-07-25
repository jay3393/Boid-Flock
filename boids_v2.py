import time
import math
import random
import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (150, 150, 150)

DEFAULT_VELOCITY = 3 # Initial velocity for all boids
MAX_VELOCITY = 1
BOID_RADIUS = 5 # The radius of a boid
VISION_RANGE = 100 # Number of pixels a boid can "see" in one direction

COHESION_COEF = 10
SEPARATION_COEF = 1
ALIGNMENT_COEF = 0.5

class Vector2d():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tuple = (x, y)

    def __repr__(self):
        """Unambiguous string representation of the vector"""
        return repr((self.x, self.y))

    def __add__(self, other):
        """Vector addition"""
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Vector subtraction"""
        return Vector2d(self.x - other.x, self.y - other.y)

    def __truediv__(self, scalar):
        """Vector division"""
        return Vector2d(self.x / scalar, self.y / scalar)

    def __mul__(self, scalar):
        """Vector multiplication by scalar"""
        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vector2d(self.x * scalar, self.y * scalar)
        raise NotImplementedError('Can only multiply Vector2D by a scalar')

    def __abs__(self):
        """Magnitude of vector"""
        return math.sqrt(self.x**2 + self.y**2)

    def __iter__(self):
        for i in self.tuple:
            yield i

    # def __lt__(self, other):
    #     """Less than comparison"""
    #     print(self.tuple, other.tuple)
    #     print(min(self.tuple[0], other.tuple[0]))
    #     return Vector2d(min(self.tuple[0], other.tuple[0]), min(self.tuple[1], other.tuple[1]))

    # def __gt__(self, other):
    #     """Greater than comparison"""
    #     return Vector2d(min(self.tuple[0], other.tuple[0]), min(self.tuple[1], other.tuple[1]))

    def distance_to(self, other):
        """Distance from one vector to another"""
        return abs(self - other)

    def to_polar(self):
        """Return the polar coordinates of vector"""
        return self.__abs__(), math.atan2(self.y, self.x)

class Boid():
    def __init__(self, position):
        self.size = BOID_RADIUS
        self.position = position
        self.velocity = Vector2d(min(DEFAULT_VELOCITY, MAX_VELOCITY), min(DEFAULT_VELOCITY, MAX_VELOCITY))
        self.vision_range = VISION_RANGE
        flock.append(self)

        self.neighbors = []
        self.color = WHITE
        self.predator = False

    def update_boid(self):
        self.get_neighbors()
        v1 = self.alignment()
        v2 = self.separation()
        v3 = self.cohesion()

        self.bound_position()

        self.velocity = self.velocity + v1 + v2 + v3
        self.position += self.velocity

        # Limit velocity, might need fixing
        if abs(self.velocity) > MAX_VELOCITY:
            self.velocity = (self.velocity / abs(self.velocity)) * MAX_VELOCITY

    def get_neighbors(self):
        for boid in flock:
            if boid not in self.neighbors and boid.position.distance_to(self.position) <= self.vision_range and boid != self:
                self.neighbors.append(boid)
                boid.neighbors.append(self)
            elif boid.position.distance_to(self.position) > self.vision_range and boid in self.neighbors:
                boid.neighbors.remove(self)
                self.neighbors.remove(boid)

    def alignment(self):
        if self.predator:
            return Vector2d(0, 0)
        v3 = Vector2d(0, 0)
        for boid in self.neighbors:
            v3 += boid.velocity

        v3 *= ALIGNMENT_COEF
        return v3

    def separation(self):
        if self.predator:
            return Vector2d(0, 0)
        v2 = Vector2d(0, 0)
        for boid in self.neighbors:
            v2 += (self.position - boid.position) / self.position.distance_to(boid.position)
            if boid.predator:
                v2 += (boid.position - self.position) * 0.005


        v2 *= SEPARATION_COEF

        return v2

    def cohesion(self):
        if self.predator:
            return Vector2d(0, 0)
        v1 = Vector2d(0, 0)
        if len(self.neighbors) == 0:
            return v1

        for boid in self.neighbors:
            v1 += boid.position

        v1 /= len(self.neighbors)
        v1 = (v1 - self.position) / COHESION_COEF

        return v1

    def bound_position(self):
        if self.position.x < 0:
            self.velocity.x += 1
        elif self.position.x > screen.width:
            self.velocity.x += -1

        if self.position.y < 0:
            self.velocity.y += 1
        elif self.position.y > screen.width:
            self.velocity.y += -1

class Canvas():
    def __init__(self, dim_x, dim_y):
        self.width, self.height = dim_x, dim_y
        self.WIN = pg.display.set_mode((self.width, self.height))
        self.columnsize, self.rowsize = 100, 100
        pg.display.flip()

    def draw_boid(self, boid):
        pg.draw.circle(self.WIN, boid.color, tuple(boid.position), boid.size)

    def draw_head(self, boid):
        pg.draw.line(self.WIN, GREEN, tuple(boid.position), tuple(boid.position + boid.velocity * 20), 1)

INPUT_SIZE = 50
screen = Canvas(1000, 1000)

flock = []
grouping = []
for x in range(INPUT_SIZE):
    grouping.append([])
    boid = Boid(Vector2d(random.choice([random.randrange(-100, -10), random.randrange(screen.width + 10, screen.width + 100)]), random.choice([random.randrange(-100, -10), random.randrange(screen.height + 10, screen.height + 100)])))
    boid.velocity = Vector2d(random.randrange(-5, 6), random.randrange(-5, 6))

predator = Boid(Vector2d(500, 500))
predator.color = RED
predator.predator = True

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.WIN.fill(BLACK)

    if pg.mouse.get_pressed()[0]:
        mousepos = pg.mouse.get_pos()
        position = Vector2d(mousepos[0], mousepos[1])
        predator.velocity += (position - predator.position) / 15

    for boid in flock:
        screen.draw_boid(boid)
        screen.draw_head(boid)
        boid.update_boid()

    pg.display.update()